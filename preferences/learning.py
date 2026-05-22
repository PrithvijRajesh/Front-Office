# Infer favorite teams/players from advanced-stat view history (per league).

from collections import Counter

from config import DEFAULT_LEAGUE_CONFIGS, NBAConfig
from preferences.store import LEAGUES, load_preferences

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


def build_league_config(league):
    """NBAConfig for one league from defaults + manual + learned preferences."""
    if league not in LEAGUES:
        raise ValueError(f"Unknown league: {league!r}")

    prefs = load_preferences()
    league_prefs = prefs[league]
    views = league_prefs.get("advanced_stat_views", [])
    defaults = DEFAULT_LEAGUE_CONFIGS[league]

    favorite_teams = list(league_prefs.get("manual_favorite_teams", []))
    favorite_players = list(league_prefs.get("manual_favorite_players", []))

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
        clutch_margin=defaults.clutch_margin,
        comeback_deficit=defaults.comeback_deficit,
        high_points=defaults.high_points,
        high_total=defaults.high_total,
    )


def build_nba_config():
    return build_league_config("nba")


def build_wnba_config():
    return build_league_config("wnba")


def is_personalization_active(league):
    return view_count_for_league(league) >= MIN_VIEWS_FOR_PERSONALIZATION


def view_count_for_league(league):
    return len(load_preferences()[league].get("advanced_stat_views", []))


def preference_summary():
    lines = ["Your preferences (per league):", ""]
    for league in LEAGUES:
        config = build_league_config(league)
        views = view_count_for_league(league)
        label = league.upper()
        lines.append(f"--- {label} ---")
        lines.append(f"  Advanced stat views: {views}")
        lines.append(
            f"  Personalized filtering: {'on' if is_personalization_active(league) else 'off'} "
            f"(after {MIN_VIEWS_FOR_PERSONALIZATION} views)"
        )
        if config.favorite_teams:
            lines.append(f"  Favorite teams: {', '.join(config.favorite_teams)}")
        if config.favorite_players:
            lines.append(f"  Favorite players: {', '.join(config.favorite_players)}")
        lines.append("")
    return "\n".join(lines).strip()
