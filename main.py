#Main code to retrieve data, use agent to exrtact only relevant information, and output results

from agent.tests.nba_game_test_data import FAKE_NBA_GAMES
from agent.decision import evaluate_nba_game
from config import NBAConfig
from agent.analysis import analyze_nba_game

configs = NBAConfig(
    favorite_teams=["Warriors", "Pistons"],
    favorite_players=["Stephen Curry", "Cade Cunningham"],
    clutch_margin=5,
    comeback_deficit=15,
    high_points=30,
    high_total=240,
)

for game in FAKE_NBA_GAMES:
    important, reasons = evaluate_nba_game(game, configs)

    print(f"{game.home_team} vs {game.away_team}: {important} -> {reasons}")

    if important:
        print("\nGame Analysis:")

        insights = analyze_nba_game(game)

        for line in insights:
            print(f"- {line}")

        print("\n" + "=" * 50 + "\n")
