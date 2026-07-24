"""Cálculo del porcentaje de partidos ganados por equipo, por temporada."""

import pandas as pd


def team_matches(matches: pd.DataFrame, team: str) -> pd.DataFrame:
    """Filtra los partidos donde el equipo jugó, de local o de visitante."""
    return matches[(matches["HomeTeam"] == team) | (matches["AwayTeam"] == team)].copy()


def _won(row: pd.Series, team: str) -> bool:
    if row["HomeTeam"] == team:
        return row["FTR"] == "H"
    return row["FTR"] == "A"


def win_rate_by_season(matches: pd.DataFrame, team: str) -> pd.DataFrame:
    """Calcula el % de partidos ganados por el equipo en cada temporada presente en `matches`."""
    played = team_matches(matches, team)
    if played.empty:
        return pd.DataFrame(columns=["Season", "Team", "Played", "Won", "WinRate"])

    played["Won"] = played.apply(_won, args=(team,), axis=1)

    summary = (
        played.groupby("Season", sort=False)
        .agg(Played=("Won", "size"), Won=("Won", "sum"))
        .reset_index()
    )
    summary["Team"] = team
    summary["WinRate"] = summary["Won"] / summary["Played"]
    return summary[["Season", "Team", "Played", "Won", "WinRate"]]
