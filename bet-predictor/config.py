"""Configuración del MVP: liga, equipos objetivo, temporadas y parámetros de la simulación."""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

LEAGUE_CODE = "SP1"  # La Liga (código de football-data.co.uk)

# Temporadas a analizar, como año de inicio (2014 -> temporada 2014/15)
SEASON_START_YEARS = list(range(2014, 2024))  # 2014/15 ... 2023/24

TARGET_TEAMS = ["Barcelona", "Real Madrid"]

STAKE = 10.0  # monto fijo apostado por partido (soles, o la unidad que se use)

# Columnas de cuotas 1X2 por prioridad: se usa el primer set completo disponible
# en cada fila, porque no todas las casas de apuestas están presentes en todas
# las temporadas.
ODDS_COLUMN_PRIORITY = [
    ("B365H", "B365D", "B365A"),
    ("BWH", "BWD", "BWA"),
    ("PSH", "PSD", "PSA"),
    ("AvgH", "AvgD", "AvgA"),
]

BASE_URL = "https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
