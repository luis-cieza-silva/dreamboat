# agents/

Espacio de experimentación con [LangChain](https://python.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/). Cada archivo es un experimento independiente (agente con memoria, tools, carga de datos, etc.).

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
uv run agents/agent1.py
```

### Dependencias actuales

- `langchain[google-genai]` — framework de agentes + integración con Gemini (`langchain-google-genai`, `langgraph`, etc.)
- `kagglehub[pandas-datasets]` — descarga de datasets de Kaggle como DataFrame de pandas
- `dotenv` — carga de variables de entorno desde `.env`

## Variables de entorno

Crear un archivo `.env` en la raíz del repo (no lo subas a git):

```
GOOGLE_GENAI_API_KEY=tu_api_key_de_gemini
KAGGLE_USERNAME=tu_usuario
KAGGLE_KEY=tu_api_key_de_kaggle
```

- `GOOGLE_GENAI_API_KEY`: se obtiene en [Google AI Studio](https://aistudio.google.com/apikey). La usan los scripts que instancian `create_agent(model="google_genai:...")`.
- `KAGGLE_USERNAME` / `KAGGLE_KEY`: credenciales de la API de Kaggle (Account → Settings → Create New Token en kaggle.com), necesarias para `kagglehub.dataset_load`.

## Problemas comunes al instalar

1. **`uv add` falla por versión de Python**: el proyecto requiere `>=3.12` (ver `requires-python` en `pyproject.toml`). Si tu Python del sistema es más viejo, corre `uv python install 3.12` y `uv sync` de nuevo.
2. **Paquetes con extras entre corchetes** (`langchain[google-genai]`, `kagglehub[pandas-datasets]`): siempre usa comillas en la shell — `uv add "langchain[google-genai]"` — porque `[]` sin comillas puede ser interpretado por zsh/bash como glob y romper el comando.
3. **Dependencias nativas pesadas** (`cryptography`, `numpy`, `pandas`): `uv` normalmente baja wheels precompilados, pero si tu plataforma no tiene wheel disponible va a intentar compilar y vas a necesitar herramientas de build (Xcode Command Line Tools en macOS: `xcode-select --install`).
4. **No mezclar `pip install` con `uv`**: si instalas algo con `pip` dentro del venv de `uv`, el `uv.lock` queda desincronizado y `uv sync` puede revertir/eliminar ese paquete. Usa siempre `uv add`.
5. **`ModuleNotFoundError` al correr con `python` directo**: los scripts deben correrse con `uv run <archivo>.py`, no con `python <archivo>.py`, para que se use el entorno virtual gestionado por `uv` (`.venv/`).
