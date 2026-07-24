"""Descarga y limpieza de datos históricos de partidos y cuotas desde football-data.co.uk."""

from pathlib import Path

import pandas as pd
import requests

from config import BASE_URL, DATA_DIR, LEAGUE_CODE, ODDS_COLUMN_PRIORITY


def _season_code(start_year: int) -> str:
    """Convierte un año de inicio de temporada (2014) al código de football-data.co.uk ('1415')."""
    end_year = start_year + 1
    return f"{str(start_year)[2:]}{str(end_year)[2:]}"


def _raw_csv_path(start_year: int) -> Path:
    return DATA_DIR / f"{LEAGUE_CODE}_{_season_code(start_year)}.csv"


def download_season(start_year: int, force: bool = False) -> Path:
    """Descarga el CSV de una temporada si no está cacheado localmente en DATA_DIR."""
    path = _raw_csv_path(start_year)
    if path.exists() and not force:
        return path

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    url = BASE_URL.format(season=_season_code(start_year), league=LEAGUE_CODE)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


def _pick_odds(row: pd.Series) -> pd.Series:
    """Elige el primer set de cuotas 1X2 completo según la prioridad configurada."""
    for home_col, draw_col, away_col in ODDS_COLUMN_PRIORITY:
        if home_col in row and pd.notna(row[home_col]) and pd.notna(row[away_col]):
            return pd.Series({"OddsH": row[home_col], "OddsD": row.get(draw_col), "OddsA": row[away_col]})
    return pd.Series({"OddsH": None, "OddsD": None, "OddsA": None})


def load_season(start_year: int) -> pd.DataFrame:
    """Carga y limpia los partidos de una temporada, agregando fecha, temporada y cuotas normalizadas."""
    path = download_season(start_year)
    df = pd.read_csv(path)

    df = df.dropna(subset=["Date", "HomeTeam", "AwayTeam", "FTR"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])

    odds = df.apply(_pick_odds, axis=1)
    season_cols = pd.DataFrame(
        {"Season": f"{start_year}/{start_year + 1}", "SeasonStartYear": start_year}, index=df.index
    )
    df = pd.concat([df, odds, season_cols], axis=1)
    df = df.dropna(subset=["OddsH", "OddsA"])

    columns = ["Date", "Season", "SeasonStartYear", "HomeTeam", "AwayTeam", "FTR", "OddsH", "OddsD", "OddsA"]
    return df[columns].sort_values("Date").reset_index(drop=True)


def load_seasons(start_years: list[int]) -> pd.DataFrame:
    """Carga y concatena varias temporadas en un único DataFrame ordenado por fecha."""
    frames = [load_season(year) for year in start_years]
    return pd.concat(frames, ignore_index=True).sort_values("Date").reset_index(drop=True)


if __name__ == "__main__":
    matches = load_seasons([2022, 2023])
    print(matches.head())
    print(f"\nTotal partidos: {len(matches)}")
