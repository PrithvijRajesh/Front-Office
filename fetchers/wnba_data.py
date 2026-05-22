# WNBA fetcher — same ESPN format as NBA; uses shared basketball mapper.

from fetchers.nba_data import (
    fetch_all_games,
    fetch_scoreboard,
    fetch_summary,
    map_to_nba_game_summary,
)


def fetch_wnba_data():
    return fetch_scoreboard("wnba")


def fetch_all_wnba_games(scoreboard_data=None):
    return fetch_all_games(scoreboard_data=scoreboard_data, league="wnba")
