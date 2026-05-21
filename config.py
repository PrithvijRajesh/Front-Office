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


def load_nba_config():
    """Config from user preference file (manual + learned from stat views)."""
    from preferences.learning import build_nba_config

    return build_nba_config()
