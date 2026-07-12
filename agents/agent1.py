import dotenv 
import os
# Load environment variables from .env file
dotenv.load_dotenv()
# Set the GOOGLE_GENAI_API_KEY environment variable in your .env file
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

from langchain.agents import create_agent
from tools import get_weather, sum_two_numbers
from system_prompt import SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver


agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather, sum_two_numbers],
    system_prompt=SYSTEM_PROMPT,
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

    print(f"Agent: {response}")