from a2a.server.apps import A2AStarletteApplication
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils.errors import ServerError, UnsupportedOperationError
from a2a.utils import new_agent_text_message
from basic_agent.langgraph_agent import graph

class LanggraphAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = graph

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        print(f"Context: {context}")
        query = context.get_user_input()
        print(f"query: {query}")
        result = self.agent.invoke({"question": query})
        print(f"result: {result}")
        await event_queue.enqueue_event(new_agent_text_message(text=result["answer"]))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())
        
    
agent_executor = LanggraphAgentExecutor()

skill = AgentSkill(
    id="langgraph_agent",
    name="langgraph_agent",
    description="A langgraph Q&A agent",
    tags=["langgraph", "qa"],
)

agent_card = AgentCard(
    name="langgraph_qa_agent",
    description="A langgraph Q&A agent",
    skills=[skill],
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    url="http://localhost:8000",
    version="1.0.0",
)

request_handler = DefaultRequestHandler(agent_executor=agent_executor, task_store=InMemoryTaskStore())

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler   
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(server.build(), host="0.0.0.0", port=8000)
