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
    system_prompt=SYSTEM_PROMPT
)

# Create a simple chat interface
chat = str(input())

result = agent.invoke(
    {"messages": [{"role": "user", "content": chat}]}
)
print(result["messages"][-1].content_blocks)