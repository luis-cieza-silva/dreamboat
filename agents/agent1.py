import dotenv 
import os
# Load environment variables from .env file
dotenv.load_dotenv()
# Set the GOOGLE_GENAI_API_KEY environment variable in your .env file
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

from langchain.agents import create_agent
from tools import get_datero_data
from system_prompt import DATERO_STATS_SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver


agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[get_datero_data],
    system_prompt=DATERO_STATS_SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)

# Config thread for memory saver
thread_config = {
    "configurable": {"thread_id": "1"}
}


# Keep the agent running to maintain the memory saver state
print("Chat with the agent (type 'exit' or 'quit' to stop):")
print("---------------------------------------------------------")
while True:
    print("You: ", end="")
    user_input = input()
    if user_input.lower() in ["exit", "quit"]:
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        thread_config
    )["messages"][-1].content

    if isinstance(response, list):
        response = "".join(
            block.get("text", "") for block in response if isinstance(block, dict)
        )

    print(f"Agent: {response}")