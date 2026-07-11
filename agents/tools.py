from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def sum(number_one: float,number_two: float) -> float:
    """Sum two numbers"""
    result = number_one + number_two
    return result