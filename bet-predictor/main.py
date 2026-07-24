"""Punto de entrada del MVP: descarga datos, calcula % de victorias y corre el backtest de apuestas."""

import argparse

import pandas as pd

from backtest import backtest_team, summarize
from config import DATA_DIR, SEASON_START_YEARS, STAKE, TARGET_TEAMS
from data_loader import load_seasons
from team_stats import win_rate_by_season


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backtest de apuestas simple para La Liga")
    parser.add_argument("--teams", nargs="+", default=TARGET_TEAMS)
    parser.add_argument("--stake", type=float, default=STAKE)
    parser.add_argument("--seasons-start", type=int, default=SEASON_START_YEARS[0])
    parser.add_argument("--seasons-end", type=int, default=SEASON_START_YEARS[-1])
    parser.add_argument("--output", default=str(DATA_DIR / "schedule.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start_years = list(range(args.seasons_start, args.seasons_end + 1))

    print(
        f"Descargando/cargando temporadas {start_years[0]}/{start_years[0] + 1} a "
        f"{start_years[-1]}/{start_years[-1] + 1}..."
    )
    matches = load_seasons(start_years)

    all_schedules = []
    for team in args.teams:
        print(f"\n=== {team} ===")

        win_rates = win_rate_by_season(matches, team)
        print(win_rates.to_string(index=False, formatters={"WinRate": "{:.1%}".format}))

        schedule = backtest_team(matches, team, args.stake)
        summary = summarize(schedule)
        if summary["bets"] == 0:
            print(f"Sin partidos encontrados para {team}.")
            continue

        print(
            f"\nApuestas: {summary['bets']} | Aciertos: {summary['wins']} "
            f"({summary['win_rate']:.1%}) | Apostado: {summary['total_staked']:.2f} | "
            f"Profit: {summary['total_profit']:.2f} | ROI: {summary['roi_pct']:.1f}%"
        )
        all_schedules.append(schedule)

    if all_schedules:
        full_schedule = pd.concat(all_schedules, ignore_index=True).sort_values("Date")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        full_schedule.to_csv(args.output, index=False)
        print(f"\nCronograma completo guardado en {args.output}")


if __name__ == "__main__":
    main()
