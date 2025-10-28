import os
from typing import Optional
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router, or_
from crewai.agent import Agent
from crewai import Crew, Task, CrewOutput
from env import OPENAI_API_KEY
from tools import web_search_tool

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class FundManagerState(BaseModel):

    # 사용자 inputs
    investment_goal: str = ""  # 사용자의 투자 목표
    risk_preference: str = ""  # 사용자의 투자 성향 (보수적, 공격적)
    budget: float = 0.0  # 사용자의 예산

    # 라우터의 의사결정
    strategy_type: str = ""

    # 분석 결과들
    tech_trends: Optional[CrewOutput] = None
    growth_scores: Optional[CrewOutput] = None
    stability_scores: Optional[CrewOutput] = None
    divide_scores: Optional[CrewOutput] = None

    portfolio: Optional[CrewOutput] = None


class FundManagerFlow(Flow[FundManagerState]):

    @start()
    def init_fund_analysis(self):
        if not self.state.investment_goal:
            raise ValueError("투자 목표를 입력해주세요")
        if not self.state.risk_preference:
            raise ValueError("투자 성향을 입력해주세요")
        if not self.state.budget:
            raise ValueError("예산을 입력해주세요")

    @listen(init_fund_analysis)
    def analyze_investment_strategy(self):
        """사용자 목표 분석"""

        strategy_router = Agent(
            role="투자 전략 라우터",
            backstory="투자 전문가로서 고객의 투자 목표와 성향을 정확히 파악하여 최적의 투자 전략팀에게 분석을 위임하는 것이 전문입니다.",
            goal="사용자의 투자 목표를 분석하여 성장주 투자인지 가치/배당주 투자인지 결정한다.",
            llm="openai/o4-mini",
        )

        analysis_result = strategy_router.kickoff(
            f"""
            사용자 투자 정보를 분석해주세요:
            - 투자 목표: {self.state.investment_goal}
            - 투자 성향: {self.state.risk_preference}
            - 투자 예산: ${self.state.budget:,.0f}

            투자 목표와 성향을 분석하여 다음 중 하나를 선택해주세요:
            1. 'growth' - 성장주 중심 투자 전략 (기술, 혁신, AI 등)
            2. 'value' - 가치/배당주 중심 투자 전략 (안정, 배당, 보수적 등)

            결과는 반드시 'growth' 또는 'value' 중 하나만 답해주세요.
            """
        )

        # Agent 결과에서 전략 추출
        analysis_text = str(analysis_result).lower()
        if "growth" in analysis_text:
            self.state.strategy_type = "growth"
        else:
            self.state.strategy_type = "value"

    @router(analyze_investment_strategy)
    def strategy_router(self):
        if self.state.strategy_type == "growth":
            return "growth_analysis"
        elif self.state.strategy_type == "value":
            return "value_analysis"

    @listen("growth_analysis")
    def analyze_tech_trends(self):
        """기술 트렌드 분석가 - 성장주 분석팀 1단계"""

        # 단일 Agent 생성
        tech_analyst = Agent(
            role="기술 트렌드 및 기업 분석가",
            backstory="""
            글로벌 기술 시장의 최신 동향을 파악하고 투자 가치가 높은 기업을 발굴하는 전문가입니다.
            시장 리포트, 뉴스, 업계 분석을 통해 떠오르는 기술 분야와 관련 상장 기업을 종합적으로 분석합니다.
            """,
            goal="사용자의 투자 목표를 기반으로 기술 트렌드를 분석하고 투자 후보 기업을 식별하여 구조화된 데이터를 제공한다.",
            tools=[web_search_tool],
            verbose=True,
        )

        # Task 1: 기술 트렌드 조사
        trend_research_task = Task(
            description=f"""
            사용자 투자 목표: {self.state.investment_goal}
            투자 성향: {self.state.risk_preference}

            현재 시장에서 주목받는 기술 트렌드를 조사하세요:

            1. "2025년 주목할 기술 트렌드" 웹 검색
            2. "혁신 기술 투자 전망" 관련 정보 수집
            3. 사용자의 투자 목표에 가장 적합한 기술 분야 3-4개 선별
            4. 각 분야의 시장 규모, 성장률, 투자 전망 분석

            결과는 다음 형식으로 정리해주세요:
            - 섹터명과 성장 가능성
            - 주요 성장 동력
            - 투자 전망 요약
            """,
            agent=tech_analyst,
            expected_output="기술 트렌드 분석 보고서 (3-4개 주요 섹터 포함)",
        )

        # Task 2: 기업 발굴
        company_discovery_task = Task(
            description="""
            이전 트렌드 분석 결과를 바탕으로 투자 후보 기업을 발굴하세요:

            1. 각 기술 섹터마다 "섹터명 관련주", "섹터명 대장주" 키워드로 웹 검색
            2. 나스닥/NYSE 상장 기업 우선 선별 (각 섹터당 최대 3개)
            3. 티커 심볼과 정확한 회사명 확인
            4. 각 기업의 사업 모델, 기술적 우위, 시장 위치 파악

            결과는 섹터별로 정리해주세요:
            - 섹터명
            - 대표 기업들 (티커, 회사명, 사업 요약)
            - 경쟁 우위와 투자 매력 포인트
            """,
            agent=tech_analyst,
            expected_output="섹터별 투자 후보 기업 리스트",
            context=[trend_research_task],
        )

        # Task 3: 데이터 구조화
        data_structuring_task = Task(
            description="""
            앞선 분석 결과를 다음 단계에서 활용할 수 있도록 구조화하세요:

            다음 JSON 배열 형식으로 정확히 응답해주세요:
            [
                {{
                    "sector": "섹터명",
                    "companies": ["TICKER1", "TICKER2", "TICKER3"],
                    "growth_potential": "성장 가능성 평가",
                    "investment_rationale": "이 섹터에 투자해야 하는 이유"
                }}
            ]

            중요한 주의사항:
            - companies 배열에는 정확한 티커 심볼만 포함
            - 각 섹터당 최대 3개 기업
            - 실제 분석된 내용만 포함
            - 마크다운 코드 블록(```)을 사용하지 말고 순수한 JSON만 반환
            - JSON 앞뒤에 어떤 텍스트도 추가하지 마세요
            - 응답은 [ 로 시작하고 ] 로 끝나야 합니다
            """,
            agent=tech_analyst,
            expected_output="""A JSON array starting with [ and ending with ]. No markdown formatting, no code blocks, no additional text. Pure JSON only.""",
            context=[trend_research_task, company_discovery_task],
            output_file="output/analyze_tech_trends.json",
        )

        tech_analysis_crew = Crew(
            agents=[tech_analyst],
            tasks=[trend_research_task, company_discovery_task, data_structuring_task],
            verbose=True,
        )

        self.state.tech_trends = tech_analysis_crew.kickoff()

    @listen(analyze_tech_trends)
    def evaluate_growth_potential(self):
        pass
        # self.state.growth_scores = ..

    @listen("value_analysis")
    def screen_stable_companies(self):
        pass
        # self.state.stability_scores = ..

    @listen(screen_stable_companies)
    def evaluate_value_potential(self):
        pass
        # self.state.divide_scores = ..

    @listen(or_(evaluate_growth_potential, evaluate_value_potential))
    def synthesize_portfolio(self):
        pass

    @listen(synthesize_portfolio)
    def finalize_investment_recommendation(self):
        pass
        return self.state.portfolio


flow = FundManagerFlow()
flow.kickoff(
    inputs={
        "investment_goal": "AI 같은 첨단 기술주에 투자하고 싶습니다.",
        "risk_preference": "공격적",
        "budget": 20000.0,
    }
)

# flow.kickoff(
#     inputs={
#         "investment_goal": "은퇴 자금을 위해 안정적인 배당을 원합니다. ",
#         "risk_preference": "보수적",
#         "budget": 50000.0,
#     }
# )


# flow.plot()
