"""Simulación de apuestas: apostar a que un equipo objetivo gana cada partido que juega."""

import pandas as pd

from team_stats import team_matches


def _bet_row(row: pd.Series, team: str, stake: float) -> dict:
    is_home = row["HomeTeam"] == team
    opponent = row["AwayTeam"] if is_home else row["HomeTeam"]
    odds = row["OddsH"] if is_home else row["OddsA"]
    won = row["FTR"] == ("H" if is_home else "A")
    profit = stake * (odds - 1) if won else -stake

    return {
        "Date": row["Date"],
        "Season": row["Season"],
        "Team": team,
        "Opponent": opponent,
        "Venue": "H" if is_home else "A",
        "Odds": odds,
        "Stake": stake,
        "Result": "W" if won else "L",
        "Profit": profit,
    }


def backtest_team(matches: pd.DataFrame, team: str, stake: float) -> pd.DataFrame:
    """Simula apostar `stake` a que `team` gana cada uno de sus partidos, en orden cronológico."""
    played = team_matches(matches, team).sort_values("Date")
    bets = [_bet_row(row, team, stake) for _, row in played.iterrows()]

    schedule = pd.DataFrame(bets)
    if schedule.empty:
        return schedule

    schedule["CumulativeProfit"] = schedule["Profit"].cumsum()
    return schedule.reset_index(drop=True)


def summarize(schedule: pd.DataFrame) -> dict:
    """Resume una tabla de apuestas: cantidad, % de aciertos, capital apostado, profit y ROI."""
    if schedule.empty:
        return {"bets": 0}

    total_bets = len(schedule)
    wins = int((schedule["Result"] == "W").sum())
    total_staked = schedule["Stake"].sum()
    total_profit = schedule["Profit"].sum()

    return {
        "team": schedule["Team"].iloc[0],
        "bets": total_bets,
        "wins": wins,
        "win_rate": wins / total_bets,
        "total_staked": total_staked,
        "total_profit": total_profit,
        "roi_pct": (total_profit / total_staked) * 100,
    }
