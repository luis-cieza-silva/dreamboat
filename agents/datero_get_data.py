"""
Módulo para importar data de Datero usando la API de Datero Hub.
"""

"""
Módulo para importar data de Datero usando la API de Datero Hub.
"""

import json

import pandas as pd
import requests


def parse_ndjson_response(response):
    """Parse NDJSON stream responses from Datero into a list of objects."""
    if not getattr(response, "text", ""):
        return []

    lines = [line.strip() for line in response.text.splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


def flatten_results(records):
    """Flatten one or more NDJSON records that contain a results list."""
    flattened = []

    for record in records:
        results = record.get("results", [])
        if isinstance(results, list):
            flattened.extend(results)

    return flattened


def datero_data(query, sources, k, return_df=True):
    """Fetch Datero search results and return them as a DataFrame or list."""
    if sources is None:
        sources = ["BCRP", "SUNAT", "INEI"]

    payload = {
        "query": query,
        "sources": sources,
        "k": k,
    }

    url_datero = "https://datero-hub.com/api/search/semantic/stream"
    response = requests.post(url_datero, json=payload, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"Error: {response.status_code} - {response.text}")

    records = parse_ndjson_response(response)
    flattened = flatten_results(records)

    if return_df:
        return pd.DataFrame(flattened)

    return flattened


if __name__ == "__main__":
    df = datero_data("exportaciones", sources=["BCRP", "SUNAT", "INEI"], k=4)
    print(df.head())
    print(f"\nTotal registros: {len(df)}")
