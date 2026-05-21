# Load/save user interaction history (advanced stat views).

import json
from datetime import datetime, timezone
from pathlib import Path

from agent.decision import _all_notable_players

PREFERENCES_PATH = Path(__file__).resolve().parent.parent / "data" / "user_preferences.json"

DEFAULT_PREFERENCES = {
    "advanced_stat_views": [],
    "manual_favorite_teams": [],
    "manual_favorite_players": [],
}


def load_preferences():
    if not PREFERENCES_PATH.exists():
        return json.loads(json.dumps(DEFAULT_PREFERENCES))

    with open(PREFERENCES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, default in DEFAULT_PREFERENCES.items():
        if key not in data:
            data[key] = list(default) if isinstance(default, list) else default
    return data


def save_preferences(data):
    PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_advanced_stat_view(game):
    """Call when the user chooses to view detailed stats for a game."""
    data = load_preferences()
    data["advanced_stat_views"].append(
        {
            "event_id": game.event_id,
            "home_team": game.home_team,
            "away_team": game.away_team,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "notable_players": [n for n in _all_notable_players(game) if n],
        }
    )
    save_preferences(data)
    return data


def view_count():
    return len(load_preferences().get("advanced_stat_views", []))
