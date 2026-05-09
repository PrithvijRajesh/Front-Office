#For nba data

'''
What ideal sports data would contain to go with preferences, brainstorming

NBA
Home Team
Away Team
Home Team Score
Away Team Score
Total Score
Clutch game?
Comeback?
Quarter score for each team (to explain game flow)
For points, assists, rebounds, steals, blocks, top player and the amount for home and away
Most impactful points player (points/minutes) for home and away team and their points
Most impactful rebounds player (rebounds/minutes) for home and away team and their reboundds
Most impactful assists player (assists/minutes) for home and away team and their assists
team percentages (field goals and three point)

'''

from dataclasses import dataclass



@dataclass
class QuarterScore:
    cumulative_score: int   # e.g. 32
    points_scored: int      # e.g. 11

@dataclass
class TeamImpactStats:
    top_points: int
    top_rebounds: int
    top_assists: int
    top_steals: int
    top_blocks: int

    top_scorer: str
    top_rebounder: str
    top_assister: str
    top_stealer: str
    top_blocker: str

    impact_points: float
    impact_points_player: str
    impact_rebounds: float
    impact_rebounds_player: str
    impact_assists: float
    impact_assists_player: str

@dataclass
class TeamAnalytics:
    q1: QuarterScore
    q2: QuarterScore
    q3: QuarterScore
    q4: QuarterScore

    fg_percent: float
    fga: int
    fgm: int

    three_p_percent: float
    three_pa: int
    three_pm: int

    turnover: int

    most_efficient_fg: float
    most_efficient_fga: int
    most_efficient_fgm: int
    most_efficient_fg_player: str

    most_efficient_3p: float
    most_efficient_3pa: int
    most_efficient_3pm: int
    most_efficient_3p_player: str

    least_efficient_fg: float
    least_efficient_fga: int
    least_efficient_fgm: int
    least_efficient_fg_player: str

    least_efficient_3p: float
    least_efficient_3pa: int
    least_efficient_3pm: int
    least_efficient_3p_player: str

    least_efficient_points: float
    least_efficient_points_player: str


@dataclass
class NBAGameSummary:
    home_team: str
    away_team: str

    home_team_score: int
    away_team_score: int
    total_score: int

    clutch_game: bool
    comeback_game: bool

    home_impact: TeamImpactStats
    away_impact: TeamImpactStats

    home_analytics: TeamAnalytics
    away_analytics: TeamAnalytics

