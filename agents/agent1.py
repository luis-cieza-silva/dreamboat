import dotenv 
import os
# Load environment variables from .env file
dotenv.load_dotenv()
# Set the GOOGLE_GENAI_API_KEY environment variable in your .env file
GEMINI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

from langchain.agents import create_agent
from tools import get_weather, sum
from system_prompt import SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver


agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather, sum],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)

# Config thread for memory saver
thread_config = {
    "configurable": {"thread_id": "1"}
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Luis"}]},
    thread_config
)["messages"][-1].content

print(response)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    thread_config
)["messages"][-1].content

print(response)