from agents import Agent, output_guardrail, Runner, RunContextWrapper, GuardrailFunctionOutput
from models import TechnicalOutputGuardRailOutput, UserAccountContext

tech_output_guardrail_agent = Agent(
    name="Technical Output Guardrail",
    instructions="""
    Analyze the technical support response to check if it inappropriately contains:
    
    - Billing information (payments, refunds, charges, subscriptions)
    - Order information (shipping, tracking, delivery, returns)
    - Account management info (passwords, email changes, account settings)
    
    Technical agents should ONLY provide technical troubleshooting, diagnostics, and product support.
    Return true for any field that contains inappropriate content for a technical support response.
    """,
    output_type=TechnicalOutputGuardRailOutput
)
    
    
@output_guardrail
async def technical_output_guardrail(wrapper: RunContextWrapper[UserAccountContext], agent: Agent, output: str) -> GuardrailFunctionOutput:
    result = await Runner.run(tech_output_guardrail_agent, output, context=wrapper.context)

    validation: TechnicalOutputGuardRailOutput = result.final_output
    triggered = validation.contains_off_topic_technical_content or validation.contains_billing_data or validation.contains_account_data

    return GuardrailFunctionOutput(output_info=validation, triggered=triggered)
