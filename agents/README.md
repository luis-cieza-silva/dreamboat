# agents/

Agente construido con [LangChain](https://python.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/) especializado en responder preguntas sobre series estadísticas peruanas (BCRP, SUNAT, INEI). Usa una sola tool: la API oficial de [Datero](https://datero-hub.com/api-docs).

- `datero_agent.py` — agente conversacional con memoria (punto de entrada).
- `datero_client.py` — cliente HTTP de la API de Datero (`GET /api/v1/search`).
- `tools.py` — tool `get_datero_data` que expone `datero_client.search` al agente.
- `system_prompt.py` — prompt del agente (`DATERO_STATS_SYSTEM_PROMPT`).

## Instalación

El proyecto usa `uv` para manejar dependencias (no `pip` directo). Todo se declara en `pyproject.toml` / `uv.lock` en la raíz del repo.

```bash
uv sync
```

Para agregar un paquete nuevo:

```bash
uv add <paquete>
```

Para ejecutar un script:

```bash
uv run agents/datero_agent.py
```

### Dependencias actuales

- `langchain[google-genai]` — framework de agentes + integración con Gemini (`langchain-google-genai`, `langgraph`, etc.)
- `requests` — cliente HTTP para la API de Datero
- `dotenv` — carga de variables de entorno desde `.env`

## Variables de entorno

Crear un archivo `.env` en la raíz del repo (no lo subas a git):

```
GEMINI_API_KEY=tu_api_key_de_gemini
DATERO_API_KEY=tu_api_key_de_datero
```

- `GEMINI_API_KEY`: se obtiene en [Google AI Studio](https://aistudio.google.com/apikey). La usa el modelo `gemini-3.7-flash` con `thinking_level="high"` (razonamiento extendido activado) que arma `datero_agent.py`.
- `DATERO_API_KEY`: se obtiene en tu cuenta de [Datero](https://datero-hub.com/api-docs). La usa `DateroClient` (header `X-API-Key`).

## Uso

El agente corre como chat interactivo en la terminal:

```bash
uv run agents/datero_agent.py
```

- Escribe tu pregunta sobre algún indicador o serie estadística peruana (ej. "dame series de pobreza monetaria") y presiona Enter.
- El agente separa tu pedido en indicadores (si pediste varios, ej. PBI y pobreza, los busca por separado) y prueba varias variantes de cada término antes de elegir. Vas a ver en la terminal cada búsqueda real que hace (`Agent: buscando "..." en ...`) y avisos de `Agent: analizando resultados...` mientras razona cuál es el mejor dataset — puede tardar bastante más que una sola consulta (varias rondas + razonamiento extendido del modelo), es normal, no se quedó colgado.
- La respuesta final lista los datasets elegidos, agrupados por indicador, con fuente y código/URL de descarga.
- El chat mantiene memoria de la conversación: podés hacer preguntas de seguimiento.
- Para salir, escribe `exit` o `quit` y presiona Enter.

## Problemas comunes al instalar

1. **`uv add` falla por versión de Python**: el proyecto requiere `>=3.12` (ver `requires-python` en `pyproject.toml`). Si tu Python del sistema es más viejo, corre `uv python install 3.12` y `uv sync` de nuevo.
2. **Paquetes con extras entre corchetes** (`langchain[google-genai]`): siempre usa comillas en la shell — `uv add "langchain[google-genai]"` — porque `[]` sin comillas puede ser interpretado por zsh/bash como glob y romper el comando.
3. **Dependencias nativas pesadas** (`cryptography`, `numpy`, `pandas`): `uv` normalmente baja wheels precompilados, pero si tu plataforma no tiene wheel disponible va a intentar compilar y vas a necesitar herramientas de build (Xcode Command Line Tools en macOS: `xcode-select --install`).
4. **No mezclar `pip install` con `uv`**: si instalas algo con `pip` dentro del venv de `uv`, el `uv.lock` queda desincronizado y `uv sync` puede revertir/eliminar ese paquete. Usa siempre `uv add`.
5. **`ModuleNotFoundError` al correr con `python` directo**: los scripts deben correrse con `uv run <archivo>.py`, no con `python <archivo>.py`, para que se use el entorno virtual gestionado por `uv` (`.venv/`).
