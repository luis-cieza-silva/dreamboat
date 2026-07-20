from langchain.tools import tool
from datero_get_data import datero_data
import pandas as pd


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def sum_two_numbers(number_one: float,number_two: float) -> float:
    """Sum two numbers"""
    result = number_one + number_two
    return result

@tool
def get_datero_data(query: str, sources: list, number_results: int) -> pd.DataFrame:
    """Get data from Datero
    This tools fetches data from Datero (website that provides data from BCRP, SUNAT, and INEI).

    Args:
        query (str): The query to search for.
        sources (list): The sources to search in. Can be a list of strings, e.g., ["BCRP", "SUNAT", "INEI"].
        number_results (int): The number of results to return.
    """
    df = datero_data(query=query, sources=sources, k=number_results, return_df=True)
    return df

# Probar tools
if __name__ == "__main__":
    print(get_datero_data.invoke({
        "query": "pobreza",
        "sources": ["BCRP", "SUNAT", "INEI"],
        "number_results": 4,
    }))