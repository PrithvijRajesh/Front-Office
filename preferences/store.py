# Load/save user interaction history (advanced stat views), per league.

import json
from datetime import datetime, timezone
from pathlib import Path

from agent.decision import _all_notable_players

PREFERENCES_PATH = Path(__file__).resolve().parent.parent / "data" / "user_preferences.json"

LEAGUES = ("nba", "wnba")

DEFAULT_LEAGUE_PREFS = {
    "advanced_stat_views": [],
    "manual_favorite_teams": [],
    "manual_favorite_players": [],
}


def _empty_preferences():
    return {league: json.loads(json.dumps(DEFAULT_LEAGUE_PREFS)) for league in LEAGUES}


def _migrate_preferences(data):
    """Support old flat JSON and new per-league structure."""
    if "nba" in data and "wnba" in data:
        return data

    if "advanced_stat_views" in data:
        migrated = _empty_preferences()
        migrated["nba"] = {
            "advanced_stat_views": data.get("advanced_stat_views", []),
            "manual_favorite_teams": data.get("manual_favorite_teams", []),
            "manual_favorite_players": data.get("manual_favorite_players", []),
        }
        for view in migrated["nba"]["advanced_stat_views"]:
            if "league" not in view:
                view["league"] = "nba"
        return migrated

    return _empty_preferences()


def load_preferences():
    if not PREFERENCES_PATH.exists():
        return _empty_preferences()

    with open(PREFERENCES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = _migrate_preferences(data)

    for league in LEAGUES:
        if league not in data:
            data[league] = json.loads(json.dumps(DEFAULT_LEAGUE_PREFS))
        for key, default in DEFAULT_LEAGUE_PREFS.items():
            if key not in data[league]:
                data[league][key] = list(default) if isinstance(default, list) else default

    return data


def save_preferences(data):
    PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_league_preferences(league):
    if league not in LEAGUES:
        raise ValueError(f"Unknown league: {league!r}")
    return load_preferences()[league]


def record_advanced_stat_view(game):
    """Call when the user chooses to view detailed stats for a game."""
    league = getattr(game, "league", "nba")
    data = load_preferences()
    data[league]["advanced_stat_views"].append(
        {
            "event_id": game.event_id,
            "league": league,
            "home_team": game.home_team,
            "away_team": game.away_team,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "notable_players": [n for n in _all_notable_players(game) if n],
        }
    )
    save_preferences(data)
    return data


def view_count(league=None):
    data = load_preferences()
    if league:
        return len(data[league].get("advanced_stat_views", []))
    return sum(len(data[l].get("advanced_stat_views", [])) for l in LEAGUES)
