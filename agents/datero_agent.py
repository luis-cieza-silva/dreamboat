import dotenv 
import os
# Load environment variables from .env file
dotenv.load_dotenv()
# Set the GEMINI_API_KEY environment variable in your .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import get_datero_data
from system_prompt import DATERO_STATS_SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver


llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", thinking_level="high")

agent = create_agent(
    model=llm,
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

    response = None
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        thread_config,
        stream_mode="updates",
    ):
        if "model" in chunk:
            ai_msg = chunk["model"]["messages"][-1]
            if ai_msg.tool_calls:
                for tool_call in ai_msg.tool_calls:
                    args = tool_call.get("args", {})
                    query = args.get("query", "?")
                    sources = args.get("sources") or []
                    print(f"Agent: buscando \"{query}\" en {', '.join(sources) if sources else 'todas las fuentes'}...")
            elif ai_msg.content:
                response = ai_msg.content
        elif "tools" in chunk:
            print("Agent: analizando resultados...")

    if isinstance(response, list):
        response = "".join(
            block.get("text", "") for block in response if isinstance(block, dict)
        )

    print(f"Agent: {response}")