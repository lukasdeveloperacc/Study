# https://github.com/langchain-ai/langchain-aws/tree/main/samples/memory
# https://docs.aws.amazon.com/ko_kr/bedrock-agentcore/latest/devguide/memory-integrate-lang.html
from dotenv import load_dotenv

load_dotenv()


from langgraph.graph import StateGraph, END, START
from langgraph.graph import MessagesState
from langgraph_checkpoint_aws import AgentCoreMemorySaver, AgentCoreMemoryStore
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import random
import string
import boto3

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def qa_node(state: MessagesState):
    message = state["messages"]
    response = llm.invoke(message)
    return {"messages": [response]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("qa", qa_node)

graph_builder.add_edge(START, "qa")
graph_builder.add_edge("qa", END)

REGION = "us-east-1"
client = boto3.client("bedrock-agentcore-control", region_name=REGION)
# random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
# name = "agentcore-" + random_suffix
# resp = client.create_memory(name=name, eventExpiryDuration=123)
# print("Memory created: ", resp)
# MEMORY_ID = resp["memoryId"]
MEMORY_ID = "memory_0izcb-6E4sWgDh99"

checkpointer = AgentCoreMemorySaver(MEMORY_ID, region_name=REGION)
store = AgentCoreMemoryStore(memory_id=MEMORY_ID, region_name=REGION)
graph = graph_builder.compile(checkpointer=checkpointer, store=store)

config = {
    "configurable": {
        "thread_id": "session-1", # REQUIRED: This maps to Bedrock AgentCore session_id under the hood
        "actor_id": "react-agent-1", # REQUIRED: This maps to Bedrock AgentCore actor_id under the hood
    }
}

def test():
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break

        response = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
        print("Agent: ", response["messages"][-1].content)
        
def check_memory():
    for checkpoint in graph.get_state_history(config):
        print(
            f"(Checkpoint ID: {checkpoint.config['configurable']['checkpoint_id']}) # of messages in state: {len(checkpoint.values.get('messages'))}"
        )

if __name__ == "__main__":
    print("Start")
    check_memory()
    # test()
