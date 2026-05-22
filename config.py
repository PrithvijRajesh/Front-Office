# Preferences: favorite teams/players, game thresholds, and learned config loader.

from dataclasses import dataclass
from typing import List


@dataclass
class NBAConfig:
    favorite_teams: List[str]
    favorite_players: List[str]
    clutch_margin: int
    comeback_deficit: int
    high_points: int
    high_total: int


DEFAULT_NBA_CONFIG = NBAConfig(
    favorite_teams=[],
    favorite_players=[],
    clutch_margin=5,
    comeback_deficit=15,
    high_points=30,
    high_total=240,
)

DEFAULT_WNBA_CONFIG = NBAConfig(
    favorite_teams=[],
    favorite_players=[],
    clutch_margin=5,
    comeback_deficit=15,
    high_points=25,
    high_total=170,
)

DEFAULT_LEAGUE_CONFIGS = {
    "nba": DEFAULT_NBA_CONFIG,
    "wnba": DEFAULT_WNBA_CONFIG,
}


def load_nba_config():
    from preferences.learning import build_league_config

    return build_league_config("nba")


def load_wnba_config():
    from preferences.learning import build_league_config

    return build_league_config("wnba")


def load_league_config(league):
    from preferences.learning import build_league_config

    return build_league_config(league)
