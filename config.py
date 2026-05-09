#To save preferences such as favorite leagues, teams, and players to follow. Also for any other preferences such as what is considered close game or high stat line.

'''
What is important to me in sports games, brainstorming

For NBA
Favorite team = Warriors and Pistons
Close games = came down to the wire, will use NBA defintion of clutch game, any game where score is within 5 points or less within last 5 minutes of 4th quarter
Comeback wins = team was down by over 15 points at some point in the game but ended up winning
High point games = player scored over 30 points,
High scoring games = total score over 240 points
Games with Playoff implications
Post season games


'''

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
    

