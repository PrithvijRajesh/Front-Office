# Main: real NBA & WNBA games from ESPN, personalized filtering, preference learning.

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from agent.analysis import analyze_nba_game
from agent.decision import evaluate_nba_game
from agent.email_digest import build_digest_body, send_nightly_email
from agent.summarizer import summarize_game
from config import load_league_config
from fetchers.nba_data import SUPPORTED_LEAGUES, fetch_all_games, fetch_all_games_for_leagues
from preferences.learning import is_personalization_active, preference_summary
from preferences.store import record_advanced_stat_view


def parse_leagues_arg(league_arg):
    if league_arg == "both":
        return SUPPORTED_LEAGUES
    if league_arg in SUPPORTED_LEAGUES:
        return (league_arg,)
    raise ValueError(f"Unknown league: {league_arg}. Use nba, wnba, or both.")


def fetch_games_for_leagues(leagues):
    if len(leagues) == len(SUPPORTED_LEAGUES):
        return fetch_all_games_for_leagues(leagues)
    games = []
    for league in leagues:
        games.extend(fetch_all_games(league=league))
    return games


def should_show_game(game):
    config = load_league_config(game.league)
    important, _ = evaluate_nba_game(game, config)
    if is_personalization_active(game.league):
        return important
    return True


def run_game_flow(games):
    if not games:
        print("No finished games on the scoreboard right now.")
        return

    print(preference_summary())
    print()

    shown = 0
    for game in games:
        if not should_show_game(game):
            continue

        config = load_league_config(game.league)
        important, reasons = evaluate_nba_game(game, config)
        shown += 1

        print("\n" + "=" * 50)
        print(f"[{game.league.upper()}] Game {shown}: {game.away_team} @ {game.home_team}")
        print(f"Final: {game.away_team_score} - {game.home_team_score}")

        if important:
            print("\nGame summary:")
            print(summarize_game(game, reasons))
        else:
            print("\nGame summary:")
            print(
                f"{game.away_team} {game.away_team_score}, "
                f"{game.home_team} {game.home_team_score}."
            )

        user_response = input("\nView advanced stats? (yes/no): ").strip().lower()
        if user_response in ("yes", "y"):
            record_advanced_stat_view(game)
            config = load_league_config(game.league)
            print("\nPreferences updated for", game.league.upper() + ".")
            print(preference_summary())
            print("\nGame analysis:")
            for line in analyze_nba_game(game):
                print(f"- {line}")

        ready = input("\nContinue to next game? (yes/no): ").strip().lower()
        if ready not in ("yes", "y"):
            break

    if shown == 0:
        print("\nNo games matched your preferences. View more advanced stats to refine favorites.")


def main():
    parser = argparse.ArgumentParser(description="Front Office — NBA & WNBA")
    parser.add_argument(
        "--league",
        choices=["nba", "wnba", "both"],
        default="both",
        help="Which league(s) to load (default: both)",
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="Send nightly email digest (requires SMTP_* and EMAIL_TO in .env)",
    )
    parser.add_argument(
        "--email-preview",
        action="store_true",
        help="Print email body without sending",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Run web UI (use SKIP_TIME_WINDOW=1 to test outside 11:59 PM–12:10 AM)",
    )
    args = parser.parse_args()

    if args.serve:
        from web.app import main as run_web

        run_web()
        return

    leagues = parse_leagues_arg(args.league)
    games = fetch_games_for_leagues(leagues)

    if args.email:
        try:
            send_nightly_email(games)
            print("Nightly email sent.")
        except RuntimeError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        return

    if args.email_preview:
        games_by_league = {}
        for game in games:
            games_by_league.setdefault(game.league, []).append(game)
        print(build_digest_body(games_by_league, leagues=leagues))
        return

    run_game_flow(games)


if __name__ == "__main__":
    main()
