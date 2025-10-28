from typing import Optional
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router, or_
from crewai import CrewOutput


class FundManagerState(BaseModel):

    # 사용자 inputs
    investment_goal: str = ""  # 사용자의 투자 목표
    risk_preference: str = ""  # 사용자의 투자 성향 (보수적, 공격적)
    budget: float = 0.0  # 사용자의 예산

    # 라우터의 의사결정
    strategy_type: str = ""

    # 분석 결과들
    tech_trends: Optional[CrewOutput] = None # CrewOutput : AI response
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
        pass
        # self.state.strategy_type = ..

    @router(analyze_investment_strategy)
    def strategy_router(self):
        if self.state.strategy_type == "growth":
            return "growth_analysis"
        elif self.state.strategy_type == "value":
            return "value_analysis"

    @listen("growth_analysis")
    def analyze_tech_trends(self):
        pass
        # self.state.tech_trends = ..

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
