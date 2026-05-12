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
        winner_4q = game.home_analytics.q4.points_scored
        winner_score = game.home_team_score
        winner_top = game.home_impact.top_scorer
        winner_top_points = game.home_impact.top_points
        loser = game.away_team
        loser_score = game.away_team_score
        loser_top = game.away_impact.top_scorer
        loser_top_points = game.away_impact.top_points
    else:
        winner = game.away_team
        winner_4q = game.away_analytics.q4.points_scored
        winner_score = game.away_team_score
        winner_top = game.away_impact.top_scorer
        winner_top_points = game.away_impact.top_points
        loser = game.home_team
        loser_score = game.home_team_score
        loser_top = game.home_impact.top_scorer
        loser_top_points = game.home_impact.top_points

    #For clutch and comeback games when top scorer on winning team and when top scorer on losing team
    if "Clutch game" in reasons and "Comeback game" in reasons:
        if winner_top_points >= loser_top_points: 
            summary = f"The {winner} rallied back to beat the {loser} {winner_score} - {loser_score} in a clutch game led by {winner_top}'s {winner_top_points} point game"
        else:
            summary = f"The {loser} caould not hold off the {winner} {loser_score} - {winner_score} comeback in a clutch game despite {loser_top}'s {loser_top_points} point game"
    elif "Comeback game" in reasons:
        if winner_top_points >= loser_top_points: 
            summary = f"The {winner} rallied back with {winner_4q} points in the fourth to beat the {loser} {winner_score} - {loser_score} led by {winner_top}'s {winner_top_points} point game"
        else:
            summary = f"The {loser} caould not hold off the {winner} {loser_score} - {winner_score} comeback despite {loser_top}'s {loser_top_points} point game"
    elif "Clutch game" in reasons:
        if winner_top_points >= loser_top_points:
            summary = f"The {winner} managed to hold off the {loser} in a tight {winner_score} - {loser_score} battle where {winner_top} dropped {winner_top_points} points"
        else:
            summary = f"{loser_top}'s {loser_top_points} point game goes to waste as the {loser} were unable to hang with the {winner} in the close {winner_score} - {loser_score} battle"
    elif any("High total score: " in r for r in reasons):
        summary = f"The {winner} vs. {loser} game was shootout where the {winner}, led by {winner_top}'s {winner_top_points} point game, beat the {loser}, led by {loser_top}'s point game, {winner_score} - {loser_score}"
    elif f"Post Season game":
        if winner_top_points >= loser_top_points:
            summary = f"The {winner} beat the {loser} {winner_score} - {loser_score} in a playoff game led by {winner_top}'s {winner_top_points} point game"
        else:
            summary = f"The {loser} lose their playoff game to the {winner} {loser_score} - {winner_score}, despite {loser_top}'s {loser_top_points} points game"
    elif f"Game has post season implication" in reasons:
        if winner_top_points >= loser_top_points:
            summary = f"The {winner} get a crucial {winner_score} - {loser_score} win against the {loser}, on the back of {winner_top}'s {winner_top_points} points"
        else:
            summary = f"Despite {loser_top}'s {loser_top_points} point effort, the {loser} drop a crucial game against the {winner}, {loser_score} - {winner_score}"
    elif any("High scoring " in r for r in reasons):
        if winner_top_points >= loser_top_points:
            summary = f"{winner_top}'s {winner_top_points} point game leads the {winner} in a {winner_score} - {loser_score} over the {loser}"
        else:
            summary = f"{loser} lose to the {winner} {loser_score} - {winner_score}, despite {loser_top} dropping {loser_top_points} points"
    else:
        summary = f"The {winner}, led by {winner_top}'s {winner_top_points} points, beat the {loser}, led by {loser_top}'s {loser_top_points} points, {winner_score} - {loser_score}"
    return summary