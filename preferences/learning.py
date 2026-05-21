# Infer favorite teams/players from advanced-stat view history.

from collections import Counter

from config import DEFAULT_NBA_CONFIG, NBAConfig
from preferences.store import load_preferences

MIN_VIEWS_FOR_PERSONALIZATION = 5
TEAM_INFERENCE_MIN_VIEWS = 5


def team_keyword(full_team_name):
    """e.g. 'Golden State Warriors' -> 'Warriors'"""
    return full_team_name.split()[-1]


def infer_favorite_teams(views, min_views=TEAM_INFERENCE_MIN_VIEWS):
    counts = Counter()
    for view in views:
        counts[team_keyword(view["home_team"])] += 1
        counts[team_keyword(view["away_team"])] += 1

    favorites = []
    for team, count in counts.most_common():
        if count >= min_views:
            favorites.append(team)
    return favorites


def infer_favorite_players(views, min_views=3):
    counts = Counter()
    for view in views:
        for name in view.get("notable_players", []):
            if name:
                counts[name] += 1

    return [name for name, count in counts.most_common() if count >= min_views]


def build_nba_config():
    """NBAConfig from defaults + manual overrides + learned preferences."""
    prefs = load_preferences()
    views = prefs.get("advanced_stat_views", [])

    favorite_teams = list(prefs.get("manual_favorite_teams", []))
    favorite_players = list(prefs.get("manual_favorite_players", []))

    if len(views) >= MIN_VIEWS_FOR_PERSONALIZATION:
        for team in infer_favorite_teams(views):
            if team not in favorite_teams:
                favorite_teams.append(team)
        for player in infer_favorite_players(views):
            if player not in favorite_players:
                favorite_players.append(player)

    return NBAConfig(
        favorite_teams=favorite_teams,
        favorite_players=favorite_players,
        clutch_margin=DEFAULT_NBA_CONFIG.clutch_margin,
        comeback_deficit=DEFAULT_NBA_CONFIG.comeback_deficit,
        high_points=DEFAULT_NBA_CONFIG.high_points,
        high_total=DEFAULT_NBA_CONFIG.high_total,
    )


def is_personalization_active():
    return len(load_preferences().get("advanced_stat_views", [])) >= MIN_VIEWS_FOR_PERSONALIZATION


def preference_summary():
    config = build_nba_config()
    views = len(load_preferences().get("advanced_stat_views", []))
    lines = [
        f"Advanced stat views recorded: {views}",
        f"Personalized filtering: {'on' if is_personalization_active() else 'off'} "
        f"(turns on after {MIN_VIEWS_FOR_PERSONALIZATION} views)",
    ]
    if config.favorite_teams:
        lines.append(f"Favorite teams (manual + inferred): {', '.join(config.favorite_teams)}")
    if config.favorite_players:
        lines.append(f"Favorite players (manual + inferred): {', '.join(config.favorite_players)}")
    return "\n".join(lines)
