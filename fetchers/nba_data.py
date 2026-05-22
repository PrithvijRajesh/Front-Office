# Sports data fetcher to return raw sports results and data

import json
import requests

from models.nba_games import (
    NBAGameSummary,
    QuarterScore,
    TeamAnalytics,
    TeamImpactStats,
)

SUPPORTED_LEAGUES = ("nba", "wnba")

CLUTCH_MARGIN = 5
COMEBACK_DEFICIT = 15


def espn_base_url(league):
    if league not in SUPPORTED_LEAGUES:
        raise ValueError(f"Unsupported league: {league!r}. Use one of {SUPPORTED_LEAGUES}")
    return f"https://site.api.espn.com/apis/site/v2/sports/basketball/{league}"


def fetch_scoreboard(league="nba"):
    url = f"{espn_base_url(league)}/scoreboard"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_nba_data():
    """Backward-compatible alias for NBA scoreboard."""
    return fetch_scoreboard("nba")


def fetch_summary(event_id, league="nba"):
    url = f"{espn_base_url(league)}/summary?event={event_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def parse_minutes(minutes_string):
    if not minutes_string or minutes_string in ("--", "-"):
        return 0.0
    if ":" in minutes_string:
        parts = minutes_string.split(":")
        return int(parts[0]) + int(parts[1]) / 60.0
    try:
        return float(minutes_string)
    except ValueError:
        return 0.0


def parse_made_attempted(display_value):
    if not display_value or "-" not in display_value:
        return 0, 0
    made, attempted = display_value.split("-")
    return int(made), int(attempted)


def stat_index(keys, name):
    return keys.index(name)


def find_players_block(summary, team_id):
    for block in summary.get("boxscore", {}).get("players") or []:
        if str(block["team"]["id"]) == str(team_id):
            return block
    return None


def build_team_impact(players_block):
    empty = TeamImpactStats(
        top_points=0,
        top_rebounds=0,
        top_assists=0,
        top_steals=0,
        top_blocks=0,
        top_scorer="",
        top_rebounder="",
        top_assister="",
        top_stealer="",
        top_blocker="",
        impact_points=0.0,
        impact_points_player="",
        impact_rebounds=0.0,
        impact_rebounds_player="",
        impact_assists=0.0,
        impact_assists_player="",
    )
    if not players_block:
        return empty

    athletes = players_block["statistics"][0]["athletes"]
    keys = players_block["statistics"][0]["keys"]
    i_pts = stat_index(keys, "points")
    i_reb = stat_index(keys, "rebounds")
    i_ast = stat_index(keys, "assists")
    i_stl = stat_index(keys, "steals")
    i_blk = stat_index(keys, "blocks")
    i_min = stat_index(keys, "minutes")

    top_points = -1
    top_rebounds = -1
    top_assists = -1
    top_steals = -1
    top_blocks = -1
    top_scorer = ""
    top_rebounder = ""
    top_assister = ""
    top_stealer = ""
    top_blocker = ""

    best_points_rate = -1.0
    best_rebounds_rate = -1.0
    best_assists_rate = -1.0
    impact_points_player = ""
    impact_rebounds_player = ""
    impact_assists_player = ""

    for player in athletes:
        if player.get("didNotPlay"):
            continue

        name = player["athlete"]["displayName"]
        stats = player["stats"]
        points = int(stats[i_pts])
        rebounds = int(stats[i_reb])
        assists = int(stats[i_ast])
        steals = int(stats[i_stl])
        blocks = int(stats[i_blk])
        minutes = parse_minutes(stats[i_min])

        if points > top_points:
            top_points = points
            top_scorer = name
        if rebounds > top_rebounds:
            top_rebounds = rebounds
            top_rebounder = name
        if assists > top_assists:
            top_assists = assists
            top_assister = name
        if steals > top_steals:
            top_steals = steals
            top_stealer = name
        if blocks > top_blocks:
            top_blocks = blocks
            top_blocker = name

        if minutes > 0:
            points_rate = points / minutes
            rebounds_rate = rebounds / minutes
            assists_rate = assists / minutes

            if points_rate > best_points_rate:
                best_points_rate = points_rate
                impact_points_player = name
            if rebounds_rate > best_rebounds_rate:
                best_rebounds_rate = rebounds_rate
                impact_rebounds_player = name
            if assists_rate > best_assists_rate:
                best_assists_rate = assists_rate
                impact_assists_player = name

    if top_points < 0:
        top_points = 0

    return TeamImpactStats(
        top_points=top_points,
        top_rebounds=max(top_rebounds, 0),
        top_assists=max(top_assists, 0),
        top_steals=max(top_steals, 0),
        top_blocks=max(top_blocks, 0),
        top_scorer=top_scorer,
        top_rebounder=top_rebounder,
        top_assister=top_assister,
        top_stealer=top_stealer,
        top_blocker=top_blocker,
        impact_points=best_points_rate if best_points_rate >= 0 else 0.0,
        impact_points_player=impact_points_player,
        impact_rebounds=best_rebounds_rate if best_rebounds_rate >= 0 else 0.0,
        impact_rebounds_player=impact_rebounds_player,
        impact_assists=best_assists_rate if best_assists_rate >= 0 else 0.0,
        impact_assists_player=impact_assists_player,
    )


def build_shooting_efficiency(players_block):
    result = {
        "most_efficient_fg": 0.0,
        "most_efficient_fga": 0,
        "most_efficient_fgm": 0,
        "most_efficient_fg_player": "",
        "most_efficient_3p": 0.0,
        "most_efficient_3pa": 0,
        "most_efficient_3pm": 0,
        "most_efficient_3p_player": "",
        "least_efficient_fg": 0.0,
        "least_efficient_fga": 0,
        "least_efficient_fgm": 0,
        "least_efficient_fg_player": "",
        "least_efficient_3p": 0.0,
        "least_efficient_3pa": 0,
        "least_efficient_3pm": 0,
        "least_efficient_3p_player": "",
        "least_efficient_points": 0.0,
        "least_efficient_points_player": "",
    }
    if not players_block:
        return result

    keys = players_block["statistics"][0]["keys"]
    i_pts = stat_index(keys, "points")
    i_fg = stat_index(keys, "fieldGoalsMade-fieldGoalsAttempted")
    i_tp = stat_index(keys, "threePointFieldGoalsMade-threePointFieldGoalsAttempted")
    i_min = stat_index(keys, "minutes")

    best_fg_pct = -1.0
    worst_fg_pct = 101.0
    best_tp_pct = -1.0
    worst_tp_pct = 101.0
    worst_points_rate = 999.0

    for player in players_block["statistics"][0]["athletes"]:
        if player.get("didNotPlay"):
            continue

        name = player["athlete"]["displayName"]
        stats = player["stats"]
        fgm, fga = parse_made_attempted(stats[i_fg])
        tpm, tpa = parse_made_attempted(stats[i_tp])
        minutes = parse_minutes(stats[i_min])
        points = int(stats[i_pts])

        if fga >= 5:
            fg_pct = fgm / fga * 100
            if fg_pct > best_fg_pct:
                best_fg_pct = fg_pct
                result["most_efficient_fg"] = fg_pct
                result["most_efficient_fga"] = fga
                result["most_efficient_fgm"] = fgm
                result["most_efficient_fg_player"] = name
            if fg_pct < worst_fg_pct:
                worst_fg_pct = fg_pct
                result["least_efficient_fg"] = fg_pct
                result["least_efficient_fga"] = fga
                result["least_efficient_fgm"] = fgm
                result["least_efficient_fg_player"] = name

        if tpa >= 3:
            tp_pct = tpm / tpa * 100
            if tp_pct > best_tp_pct:
                best_tp_pct = tp_pct
                result["most_efficient_3p"] = tp_pct
                result["most_efficient_3pa"] = tpa
                result["most_efficient_3pm"] = tpm
                result["most_efficient_3p_player"] = name
            if tp_pct < worst_tp_pct:
                worst_tp_pct = tp_pct
                result["least_efficient_3p"] = tp_pct
                result["least_efficient_3pa"] = tpa
                result["least_efficient_3pm"] = tpm
                result["least_efficient_3p_player"] = name

        if minutes > 0:
            points_rate = points / minutes
            if points_rate < worst_points_rate:
                worst_points_rate = points_rate
                result["least_efficient_points"] = points_rate
                result["least_efficient_points_player"] = name

    return result


def clock_seconds_left(clock_display):
    if not clock_display:
        return None
    if ":" in clock_display:
        mins, secs = clock_display.split(":")
        return int(mins) * 60 + float(secs)
    return float(clock_display)


def detect_clutch_game(plays, margin=CLUTCH_MARGIN):
    for play in plays:
        period = play.get("period", {})
        if period.get("number") != 4:
            continue

        seconds_left = clock_seconds_left(play.get("clock", {}).get("displayValue"))
        if seconds_left is None or seconds_left > 300:
            continue

        home_score = int(play["homeScore"])
        away_score = int(play["awayScore"])
        if abs(home_score - away_score) <= margin:
            return True
    return False


def detect_comeback_game(home_score, away_score, home_competitor, away_competitor, deficit=COMEBACK_DEFICIT):
    home_running = 0
    away_running = 0

    for period in range(1, 5):
        for quarter in home_competitor.get("linescores", []):
            if quarter["period"] == period:
                home_running = home_running + int(quarter["value"])
        for quarter in away_competitor.get("linescores", []):
            if quarter["period"] == period:
                away_running = away_running + int(quarter["value"])

        score_diff = home_running - away_running

        if home_score > away_score and score_diff <= -deficit:
            return True
        if away_score > home_score and score_diff >= deficit:
            return True

    return False


def map_quarters_from_competitor(competitor):
    q1 = QuarterScore(cumulative_score=0, points_scored=0)
    q2 = QuarterScore(cumulative_score=0, points_scored=0)
    q3 = QuarterScore(cumulative_score=0, points_scored=0)
    q4 = QuarterScore(cumulative_score=0, points_scored=0)

    for quarter in competitor.get("linescores", []):
        period = quarter["period"]
        points = int(quarter["value"])
        if period == 1:
            q1.points_scored = points
            q1.cumulative_score = points
        if period == 2:
            q2.points_scored = points
            q2.cumulative_score = q1.cumulative_score + points
        if period == 3:
            q3.points_scored = points
            q3.cumulative_score = q2.cumulative_score + points
        if period == 4:
            q4.points_scored = points
            q4.cumulative_score = q3.cumulative_score + points

    return q1, q2, q3, q4


def map_to_nba_game_summary(event, summary, league="nba"):
    competitors = event["competitions"][0]["competitors"]

    home_competitor = None
    away_competitor = None
    for competitor in competitors:
        if competitor["homeAway"] == "home":
            home_competitor = competitor
        if competitor["homeAway"] == "away":
            away_competitor = competitor

    home_team = home_competitor["team"]["displayName"]
    away_team = away_competitor["team"]["displayName"]
    home_team_score = int(home_competitor["score"])
    away_team_score = int(away_competitor["score"])
    total_score = home_team_score + away_team_score

    post_season = event["season"]["slug"] == "post-season"
    post_season_impact = post_season

    boxscore_teams = summary["boxscore"]["teams"]
    home_box = None
    away_box = None
    for team in boxscore_teams:
        if team["homeAway"] == "home":
            home_box = team
        if team["homeAway"] == "away":
            away_box = team

    homeFGM = 0
    homeFGA = 0
    homeTPM = 0
    homeTPA = 0
    home_turnovers = 0
    for stat in home_box["statistics"]:
        if stat["name"] == "fieldGoalsMade-fieldGoalsAttempted":
            homeFGM, homeFGA = parse_made_attempted(stat["displayValue"])
        if stat["name"] == "threePointFieldGoalsMade-threePointFieldGoalsAttempted":
            homeTPM, homeTPA = parse_made_attempted(stat["displayValue"])
        if stat["name"] == "turnovers":
            home_turnovers = int(stat["displayValue"])

    awayFGM = 0
    awayFGA = 0
    awayTPM = 0
    awayTPA = 0
    away_turnovers = 0
    for stat in away_box["statistics"]:
        if stat["name"] == "fieldGoalsMade-fieldGoalsAttempted":
            awayFGM, awayFGA = parse_made_attempted(stat["displayValue"])
        if stat["name"] == "threePointFieldGoalsMade-threePointFieldGoalsAttempted":
            awayTPM, awayTPA = parse_made_attempted(stat["displayValue"])
        if stat["name"] == "turnovers":
            away_turnovers = int(stat["displayValue"])

    if homeFGA > 0:
        home_fg_percent = homeFGM / homeFGA * 100
    else:
        home_fg_percent = 0

    if homeTPA > 0:
        home_three_p_percent = homeTPM / homeTPA * 100
    else:
        home_three_p_percent = 0

    if awayFGA > 0:
        away_fg_percent = awayFGM / awayFGA * 100
    else:
        away_fg_percent = 0

    if awayTPA > 0:
        away_three_p_percent = awayTPM / awayTPA * 100
    else:
        away_three_p_percent = 0

    home_q1, home_q2, home_q3, home_q4 = map_quarters_from_competitor(home_competitor)
    away_q1, away_q2, away_q3, away_q4 = map_quarters_from_competitor(away_competitor)

    home_players = find_players_block(summary, home_box["team"]["id"])
    away_players = find_players_block(summary, away_box["team"]["id"])

    home_impact = build_team_impact(home_players)
    away_impact = build_team_impact(away_players)

    home_eff = build_shooting_efficiency(home_players)
    away_eff = build_shooting_efficiency(away_players)

    plays = summary.get("plays") or []
    clutch_game = detect_clutch_game(plays)
    comeback_game = detect_comeback_game(
        home_team_score, away_team_score, home_competitor, away_competitor
    )

    home_analytics = TeamAnalytics(
        q1=home_q1,
        q2=home_q2,
        q3=home_q3,
        q4=home_q4,
        fg_percent=home_fg_percent,
        fga=homeFGA,
        fgm=homeFGM,
        three_p_percent=home_three_p_percent,
        three_pa=homeTPA,
        three_pm=homeTPM,
        turnover=home_turnovers,
        **home_eff,
    )

    away_analytics = TeamAnalytics(
        q1=away_q1,
        q2=away_q2,
        q3=away_q3,
        q4=away_q4,
        fg_percent=away_fg_percent,
        fga=awayFGA,
        fgm=awayFGM,
        three_p_percent=away_three_p_percent,
        three_pa=awayTPA,
        three_pm=awayTPM,
        turnover=away_turnovers,
        **away_eff,
    )

    return NBAGameSummary(
        home_team=home_team,
        away_team=away_team,
        home_team_score=home_team_score,
        away_team_score=away_team_score,
        total_score=total_score,
        clutch_game=clutch_game,
        comeback_game=comeback_game,
        post_season=post_season,
        post_season_impact=post_season_impact,
        home_impact=home_impact,
        away_impact=away_impact,
        home_analytics=home_analytics,
        away_analytics=away_analytics,
        league=league,
        event_id=event.get("id", ""),
    )


def get_finished_events(scoreboard_data):
    """Events on the scoreboard that already have a score."""
    finished = []
    for event in scoreboard_data.get("events", []):
        competitors = event["competitions"][0]["competitors"]
        scores = [int(c["score"]) for c in competitors]
        if scores[0] > 0 or scores[1] > 0:
            finished.append(event)
    return finished


def fetch_all_games(scoreboard_data=None, league="nba"):
    """Map every finished game on the scoreboard to NBAGameSummary."""
    if scoreboard_data is None:
        scoreboard_data = fetch_scoreboard(league)

    games = []
    for event in get_finished_events(scoreboard_data):
        summary = fetch_summary(event["id"], league=league)
        games.append(map_to_nba_game_summary(event, summary, league=league))
    return games


def fetch_all_games_for_leagues(leagues=SUPPORTED_LEAGUES):
    """Fetch finished games for multiple leagues (e.g. NBA + WNBA)."""
    all_games = []
    for league in leagues:
        all_games.extend(fetch_all_games(league=league))
    return all_games


# Run this file to test: python -m fetchers.nba_data
if __name__ == "__main__":
    games = fetch_all_games_for_leagues()
    if not games:
        print("No games with scores on the scoreboard yet.")
        exit()

    print(f"Loaded {len(games)} finished game(s).\n")
    for game in games:
        print(
            f"[{game.league.upper()}]",
            game.away_team,
            "@",
            game.home_team,
            "—",
            game.away_team_score,
            "-",
            game.home_team_score,
        )
