from agents import Agent, RunContextWrapper, input_guardrail, Runner, GuardrailFunctionOutput, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX # When your agent has handoff
from agents.extensions import handoff_filters
from models import UserAccountContext, InputGuardRailOutput, HandoffData
from my_agents.account_agent import account_agent
from my_agents.billing_agent import billing_agent
from my_agents.order_agent import order_agent
from my_agents.technical_agent import technical_agent

import streamlit as st

input_guardrail_agent = Agent(
    name="Input Guardrail Agent", 
    instructions="""Ensure the user's request specifically pertains to User Account details, Billing inquiries, Order information, or Technical Support issues, and is not off-topic.
    If the request is off-topic, return a reason for the tripwire. You can make small conversation with the user, specially at the beginning of the conversation, but don't help with requests that are not related to User Account details, Billing inquiries, Order information, or Technical Support issues.""",
    output_type=InputGuardRailOutput)

@input_guardrail
async def off_topic_guardrail(wrapper: RunContextWrapper[UserAccountContext], agent: Agent[UserAccountContext], input: str) -> InputGuardRailOutput:
    result = await Runner.run(input_guardrail_agent, input, context=wrapper.context)
    # if is_off_topic is true, raise error

    return GuardrailFunctionOutput(output_info=result.final_output, tripwire_triggered=result.final_output.is_off_topic)

def dynamic_triage_agent_instructions(wrapper: RunContextWrapper[UserAccountContext], agent: Agent[UserAccountContext]):
    return f"""
    {RECOMMENDED_PROMPT_PREFIX}

    You are a customer support agent. You ONLY help customers with their questions about their User Account, Billing, Orders, or Technical Support.
    You call customers by their name.
    
    The customer's name is {wrapper.context.name}.
    The customer's email is {wrapper.context.email}.
    The customer's tier is {wrapper.context.tier}.
    
    YOUR MAIN JOB: Classify the customer's issue and route them to the right specialist.
    
    ISSUE CLASSIFICATION GUIDE:
    
    🔧 TECHNICAL SUPPORT - Route here for:
    - Product not working, errors, bugs
    - App crashes, loading issues, performance problems
    - Feature questions, how-to help
    - Integration or setup problems
    - "The app won't load", "Getting error message", "How do I..."
    
    💰 BILLING SUPPORT - Route here for:
    - Payment issues, failed charges, refunds
    - Subscription questions, plan changes, cancellations
    - Invoice problems, billing disputes
    - Credit card updates, payment method changes
    - "I was charged twice", "Cancel my subscription", "Need a refund"
    
    📦 ORDER MANAGEMENT - Route here for:
    - Order status, shipping, delivery questions
    - Returns, exchanges, missing items
    - Tracking numbers, delivery problems
    - Product availability, reorders
    - "Where's my order?", "Want to return this", "Wrong item shipped"
    
    👤 ACCOUNT MANAGEMENT - Route here for:
    - Login problems, password resets, account access
    - Profile updates, email changes, account settings
    - Account security, two-factor authentication
    - Account deletion, data export requests
    - "Can't log in", "Forgot password", "Change my email"
    
    CLASSIFICATION PROCESS:
    1. Listen to the customer's issue
    2. Ask clarifying questions if the category isn't clear
    3. Classify into ONE of the four categories above
    4. Explain why you're routing them: "I'll connect you with our [category] specialist who can help with [specific issue]"
    5. Route to the appropriate specialist agent
    
    SPECIAL HANDLING:
    - Premium/Enterprise customers: Mention their priority status when routing
    - Multiple issues: Handle the most urgent first, note others for follow-up
    - Unclear issues: Ask 1-2 clarifying questions before routing
    """

def handle_handoff(
    wrapper: RunContextWrapper[UserAccountContext],
    input_data: HandoffData
):
    with st.sidebar:
        st.write(f"""
            Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.issue_type}
            Description: {input_data.issue_description}
        """)

def make_handoff(agent):
    return handoff(
        agent=agent, 
        on_handoff=handle_handoff, 
        input_type=HandoffData, 
        input_filter=handoff_filters.remove_all_tools # extensions 중 tool 메시지들만 삭제해주는 녀석.
    )

triage_agent = Agent(
    name="Triage Agent", 
    instructions=dynamic_triage_agent_instructions, 
    input_guardrails=[off_topic_guardrail], 
    # handoff가 되면 이전 agent와 대화가 종료되고, 인계 받은 에이전트와 메시지를 공유할 수 있도록 함
    handoffs=[
        make_handoff(account_agent), 
        make_handoff(billing_agent), 
        make_handoff(order_agent), 
        make_handoff(technical_agent)
    ], 
    # 대화를 종료시키고 싶지 않다면, tools로 정의한다.
    # tools=[technical_agent.as_tool(tool_name="Technical Support". tool_description="Use this when the user needs tech support.")]
)
