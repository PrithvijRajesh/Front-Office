# Sports data fetcher to return raw sports results and data

import json
import requests

from models.nba_games import (
    NBAGameSummary,
    QuarterScore,
    TeamAnalytics,
    TeamImpactStats,
)

baseURL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"


def fetch_nba_data():
    url = f"{baseURL}/scoreboard"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_summary(event_id):
    url = f"{baseURL}/summary?event={event_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def map_to_nba_game_summary(event, summary):
    """
    Turn ESPN event + summary JSON into one NBAGameSummary.
    Fill in the TODO sections as you go.
    """

    # --- From scoreboard event: teams and scores ---
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

    if event["season"]["slug"] == "post-season":
        post_season = True
    else:
        post_season = False

    # --- From summary boxscore: match home/away teams ---
    boxscore_teams = summary["boxscore"]["teams"]

    home_box = None
    away_box = None
    for team in boxscore_teams:
        if team["homeAway"] == "home":
            home_box = team
        if team["homeAway"] == "away":
            away_box = team

    # --- Team shooting stats (same idea as your stats1 / stats2 code) ---
    homeFGM = 0
    homeFGA = 0
    homeTPM = 0
    homeTPA = 0
    home_turnovers = 0

    for stat in home_box["statistics"]:
        if stat["name"] == "fieldGoalsMade-fieldGoalsAttempted":
            homeFGM, homeFGA = stat["displayValue"].split("-")
            homeFGM = int(homeFGM)
            homeFGA = int(homeFGA)
        if stat["name"] == "threePointFieldGoalsMade-threePointFieldGoalsAttempted":
            homeTPM, homeTPA = stat["displayValue"].split("-")
            homeTPM = int(homeTPM)
            homeTPA = int(homeTPA)
        if stat["name"] == "turnovers":
            home_turnovers = int(stat["displayValue"])

    awayFGM = 0
    awayFGA = 0
    awayTPM = 0
    awayTPA = 0
    away_turnovers = 0

    for stat in away_box["statistics"]:
        if stat["name"] == "fieldGoalsMade-fieldGoalsAttempted":
            awayFGM, awayFGA = stat["displayValue"].split("-")
            awayFGM = int(awayFGM)
            awayFGA = int(awayFGA)
        if stat["name"] == "threePointFieldGoalsMade-threePointFieldGoalsAttempted":
            awayTPM, awayTPA = stat["displayValue"].split("-")
            awayTPM = int(awayTPM)
            awayTPA = int(awayTPA)
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

    # --- Quarter scores (TODO: you fill this in) ---
    # home_competitor["linescores"] has one entry per quarter
    # each entry has displayValue = points in that quarter
    empty_quarter = QuarterScore(cumulative_score=0, points_scored=0)

    home_q1 = empty_quarter
    home_q2 = empty_quarter
    home_q3 = empty_quarter
    home_q4 = empty_quarter

    for quarters in home_box["linescores"]:
        if quarters["period"] == 1:
            home_q1.cumulative_score, home_q1.points_scored = int(quarters["value"]),int(quarters["value"])
        if quarters["period"] == 2:
            home_q2.cumulative_score, home_q2.points_scored = int(quarters["value"])+home_q1.cumulative_score,int(quarters["value"])
        if quarters["period"] == 3:
            home_q2.cumulative_score, home_q2.points_scored = int(quarters["value"])+home_q2.cumulative_score,int(quarters["value"])
        if quarters["period"] == 4:
            home_q2.cumulative_score, home_q2.points_scored = int(quarters["value"])+home_q3.cumulative_score,int(quarters["value"])

    away_q1 = empty_quarter
    away_q2 = empty_quarter
    away_q3 = empty_quarter
    away_q4 = empty_quarter

    for quarters in away_box["linescores"]:
        if quarters["period"] == 1:
            away_q1.cumulative_score, away_q1.points_scored = int(quarters["value"]),int(quarters["value"])
        if quarters["period"] == 2:
            away_q2.cumulative_score, away_q2.points_scored = int(quarters["value"])+away_q1.cumulative_score,int(quarters["value"])
        if quarters["period"] == 3:
            away_q2.cumulative_score, away_q2.points_scored = int(quarters["value"])+away_q2.cumulative_score,int(quarters["value"])
        if quarters["period"] == 4:
            away_q2.cumulative_score, away_q2.points_scored = int(quarters["value"])+away_q3.cumulative_score,int(quarters["value"])

    # --- Player stats like top scorer (TODO: you fill this in) ---
    empty_impact = TeamImpactStats(
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

    home_impact = empty_impact
    away_impact = empty_impact

    # --- Build TeamAnalytics objects ---
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
        most_efficient_fg=0.0,
        most_efficient_fga=0,
        most_efficient_fgm=0,
        most_efficient_fg_player="",
        most_efficient_3p=0.0,
        most_efficient_3pa=0,
        most_efficient_3pm=0,
        most_efficient_3p_player="",
        least_efficient_fg=0.0,
        least_efficient_fga=0,
        least_efficient_fgm=0,
        least_efficient_fg_player="",
        least_efficient_3p=0.0,
        least_efficient_3pa=0,
        least_efficient_3pm=0,
        least_efficient_3p_player="",
        least_efficient_points=0.0,
        least_efficient_points_player="",
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
        most_efficient_fg=0.0,
        most_efficient_fga=0,
        most_efficient_fgm=0,
        most_efficient_fg_player="",
        most_efficient_3p=0.0,
        most_efficient_3pa=0,
        most_efficient_3pm=0,
        most_efficient_3p_player="",
        least_efficient_fg=0.0,
        least_efficient_fga=0,
        least_efficient_fgm=0,
        least_efficient_fg_player="",
        least_efficient_3p=0.0,
        least_efficient_3pa=0,
        least_efficient_3pm=0,
        least_efficient_3p_player="",
        least_efficient_points=0.0,
        least_efficient_points_player="",
    )

    game = NBAGameSummary(
        home_team=home_team,
        away_team=away_team,
        home_team_score=home_team_score,
        away_team_score=away_team_score,
        total_score=total_score,
        clutch_game=False,
        comeback_game=False,
        post_season=post_season,
        post_season_impact=False,
        home_impact=home_impact,
        away_impact=away_impact,
        home_analytics=home_analytics,
        away_analytics=away_analytics,
    )

    return game


# Run this file to test: python -m fetchers.nba_data
if __name__ == "__main__":
    data = fetch_nba_data()
    events = data["events"]
    first_game = events[0]
    event_id = first_game["id"]

    summary = fetch_summary(event_id)
    game = map_to_nba_game_summary(first_game, summary)

    print(game.home_team, "vs", game.away_team)
    print(game.home_team_score, "-", game.away_team_score)
    print("Home FG%:", game.home_analytics.fg_percent)
    with open("fetchers/nba_data.json", "w") as f:
        json.dump(first_game, f, indent=2)

