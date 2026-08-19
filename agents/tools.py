from langchain.tools import tool
from datero_client import DateroClient

datero_client = DateroClient()


@tool
def get_datero_data(query: str, sources: list, number_results: int) -> list[dict]:
    """Get data from Datero
    This tools fetches data from Datero (website that provides data from BCRP, SUNAT, and INEI)
    using the official Datero API (https://datero-hub.com/api-docs).

    Args:
        query (str): The query to search for.
        sources (list): The sources to search in. Can be a list of strings, e.g., ["BCRP", "SUNAT", "INEI"].
        number_results (int): The number of results to return.
    """
    resultado = datero_client.search(q=query, sources=sources, limit=number_results)
    return resultado["data"]

# Probar tools
if __name__ == "__main__":
    print(get_datero_data.invoke({
        "query": "pobreza",
        "sources": ["BCRP", "SUNAT", "INEI"],
        "number_results": 4,
    }))