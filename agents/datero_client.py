"""
Cliente para la API oficial de Datero Hub (https://datero-hub.com/api-docs).

Requiere la variable de entorno DATERO_API_KEY (definida en .env).
"""

import os

import dotenv
import requests

dotenv.load_dotenv()

BASE_URL = "https://datero-hub.com/api/v1"


class DateroClient:
    """Cliente HTTP para la API oficial de Datero (búsqueda semántica de series)."""

    def __init__(self, api_key: str = None, base_url: str = BASE_URL, timeout: int = 30):
        self.api_key = api_key or os.getenv("DATERO_API_KEY")
        if not self.api_key:
            raise ValueError("Falta DATERO_API_KEY (defínela en tu .env).")
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": self.api_key})

    def _get(self, path: str, params: dict = None) -> dict:
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def search(self, q: str, sources: list = None, limit: int = 4) -> dict:
        """Búsqueda semántica de series y publicaciones.

        Args:
            q: consulta en lenguaje natural (2-500 caracteres).
            sources: lista de fuentes, e.g. ["BCRP", "SUNAT", "INEI"].
            limit: resultados por fuente (máx 10, default 4).
        """
        params = {"q": q, "limit": limit}
        if sources:
            params["sources"] = ",".join(sources)
        return self._get("/search", params=params)


if __name__ == "__main__":
    client = DateroClient()
    resultado = client.search(q="petroleo", sources=["BCRP"], limit=5)
    for serie in resultado["data"]:
        print(serie["source"], serie["codigo"], serie["title"])
