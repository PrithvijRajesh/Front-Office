#Used to give brief explanation of games and allow user to decide if game is important or not

"""
Hierarchy of games
Clutch and comeback games
Comeback games
Clutch games
High player points
High total points
Battle of Stars
Playoff games
PLay off implication games
Generic games
"""

def summarize_game(game, reasons):
    summary = ""
    winner = ""
    winner_score = ""
    loser = ""
    loser_score = ""
    winner_top = ""
    loser_top = ""
    winner_top_points = ""
    loser_top_points = ""
    if game.home_team_score > game.away_team_score:
        winner = game.home_team
        winner_score = game.home_team_score
        winner_top = game.home_impact.top_scorer
        winner_top_points = game.home_impact.top_points
        loser = game.away_team
        loser_score = game.away_team_score
        loser_top = game.away_impact.top_scorer
        loser_top_points = game.away_impact.top_points
    else:
        winner = game.away_team
        winner_score = game.away_team_score
        winner_top = game.away_impact.top_scorer
        winner_top_points = game.away_impact.top_points
        loser = game.home_team
        loser_score = game.home_team_score
        loser_top = game.home_impact.top_scorer
        loser_top_points = game.home_impact.top_points

    #For clutch and comeback games when top scorer on winning team and when top scorer on losing team
    if winner_top_points>= loser_top_points and "Clutch game" in reasons and "Comeback game" in reasons:
        summary = f"The {winner} rallied back to beat the {loser} {winner_score} - {loser_score} in a clutch game led by {winner_top}'s {winner_top_points} point game"
    elif winner_top_points< loser_top_points and "Clutch game" in reasons and "Comeback game" in reasons:
        summary = f"The {loser} cannot hold off the {winner} {loser_score} - {winner_score} in a clutch game despite {winner_top}'s {winner_top_points} point game"
    return summary