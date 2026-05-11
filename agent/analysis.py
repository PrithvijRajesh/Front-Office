def analyze_nba_game(game):
    insights = []

    # Teams
    insights.append(f"{game.home_team} vs {game.away_team}")

    # Score
    insights.append(
        f"Score: {game.home_team}: {game.home_team_score} - {game.away_team}: {game.away_team_score}"
    )

    #Quarter by Quarter breakdown
    insights.append (
        f"Quarter by Quarter Scores "
    )
    insights.append (
        f"Quarter 1: {game.home_analytics.q1.cumulative_score} - {game.away_analytics.q1.cumulative_score} "
    )
    insights.append (
        f"Quarter 2: {game.home_analytics.q2.cumulative_score} - {game.away_analytics.q2.cumulative_score} "
    )
    insights.append (
        f"Quarter 3: {game.home_analytics.q3.cumulative_score} - {game.away_analytics.q3.cumulative_score} "
    )
    insights.append (
        f"Quarter 4: {game.home_analytics.q4.cumulative_score} - {game.away_analytics.q4.cumulative_score} "
    )

    #Points scored each Quarter
    insights.append (
        f"Points scored each quarter"
    )
    insights.append (
        f"Quarter 1: {game.home_analytics.q1.points_scored} - {game.away_analytics.q1.points_scored} "
    )
    insights.append (
        f"Quarter 2: {game.home_analytics.q2.points_scored} - {game.away_analytics.q2.points_scored} "
    )
    insights.append (
        f"Quarter 3: {game.home_analytics.q3.points_scored} - {game.away_analytics.q3.points_scored} "
    )
    insights.append (
        f"Quarter 4: {game.home_analytics.q4.points_scored} - {game.away_analytics.q4.points_scored} "
    )


    #Home team stats
    insights.append (
        f"Stats for home team: {game.home_team}"
    )

    # Top players for home team
    insights.append (
        f"Stat leaders"
    )
    insights.append(
        f"{game.home_impact.top_scorer} scored {game.home_impact.top_points} pts"
    )
    insights.append (
        f"{game.home_impact.top_rebounder} grabbed {game.home_impact.top_rebounds} rebounds "
    )
    insights.append (
        f"{game.home_impact.top_assister} had {game.home_impact.top_assists} assists "
    )
    insights.append (
        f"{game.home_impact.top_blocker} blocked {game.home_impact.top_blocks} shots "
    )
    insights.append (
        f"{game.home_impact.top_stealer} had {game.home_impact.top_steals} steals"
    )

    #Home impact players
    insights.append(
        f"Most impactful players by stats"
    )
    insights.append(
        f"{game.home_impact.impact_points_player} scored at a rate of {game.home_impact.impact_points} points per minute"
    )
    insights.append(
        f"{game.home_impact.impact_rebounds_player} rebounded at a rate of {game.home_impact.impact_rebounds} rebounds per minute"
    )
    insights.append(
        f"{game.home_impact.impact_assists_player} assisted at a rate of {game.home_impact.impact_assists} assists per minute"
    )

    #Home team analytics
    insights.append (
        f"Analytics"
    )
    insights.append (
        f"Field Goal Percentage: {game.home_analytics.fg_percent}%"
    )
    insights.append (
        f"Field Goals Attemped: {game.home_analytics.fga} shots"
    )
    insights.append (
        f"Field Goals Made: {game.home_analytics.fgm} shots"
    )
    insights.append (
        f"Three Point Percentage: {game.home_analytics.three_p_percent}%"
    )
    insights.append (
        f"Three Pointers Attempted: {game.home_analytics.three_pa} threes"
    )
    insights.append (
        f"Three Pointers Made: {game.home_analytics.three_pm} threes"
    )
    insights.append (
        f"Turnovers: {game.home_analytics.turnover} turnovers"
    )
    insights.append (
        f"Most efficient field goal shooter: {game.home_analytics.most_efficient_fg_player}"
    )
    insights.append (
        f"  {game.home_analytics.most_efficient_fg}% on {game.home_analytics.most_efficient_fgm} of {game.home_analytics.most_efficient_fga} shots" 
    )
    insights.append (
        f"Most efficient three point shooter: {game.home_analytics.most_efficient_3p_player}"
    )
    insights.append (
        f"  {game.home_analytics.most_efficient_3p}% on {game.home_analytics.most_efficient_3pm} of {game.home_analytics.most_efficient_3pa} threes" 
    )
    insights.append (
        f"Least efficient field goal shooter: {game.home_analytics.least_efficient_fg_player}"
    )
    insights.append (
        f"  {game.home_analytics.least_efficient_fg}% on {game.home_analytics.least_efficient_fgm} of {game.home_analytics.least_efficient_fga} shots" 
    )
    insights.append (
        f"Least efficient three point shooter: {game.home_analytics.least_efficient_3p_player}"
    )
    insights.append (
        f"  {game.home_analytics.least_efficient_3p}% on {game.home_analytics.least_efficient_3pm} of {game.home_analytics.least_efficient_3pa} threes" 
    )
    insights.append (
        f"Least impactful player based on points was {game.home_analytics.least_efficient_points_player} who scored at a rate of {game.home_analytics.least_efficient_points} points per minute"
    )

    #away team stats
    insights.append (
        f"Stats for away team: {game.away_team}"
    )

    # Top players for away team
    insights.append (
        f"Stat leaders"
    )
    insights.append(
        f"{game.away_impact.top_scorer} scored {game.away_impact.top_points} pts"
    )
    insights.append (
        f"{game.away_impact.top_rebounder} grabbed {game.away_impact.top_rebounds} rebounds "
    )
    insights.append (
        f"{game.away_impact.top_assister} had {game.away_impact.top_assists} assists "
    )
    insights.append (
        f"{game.away_impact.top_blocker} blocked {game.away_impact.top_blocks} shots "
    )
    insights.append (
        f"{game.away_impact.top_stealer} had {game.away_impact.top_steals} steals"
    )

    #away impact players
    insights.append(
        f"Most impactful players by stats"
    )
    insights.append(
        f"{game.away_impact.impact_points_player} scored at a rate of {game.away_impact.impact_points} points per minute"
    )
    insights.append(
        f"{game.away_impact.impact_rebounds_player} rebounded at a rate of {game.away_impact.impact_rebounds} rebounds per minute"
    )
    insights.append(
        f"{game.away_impact.impact_assists_player} assisted at a rate of {game.away_impact.impact_assists} assists per minute"
    )

    #away team analytics
    insights.append (
        f"Analytics"
    )
    insights.append (
        f"Field Goal Percentage: {game.away_analytics.fg_percent}%"
    )
    insights.append (
        f"Field Goals Attemped: {game.away_analytics.fga} shots"
    )
    insights.append (
        f"Field Goals Made: {game.away_analytics.fgm} shots"
    )
    insights.append (
        f"Three Point Percentage: {game.away_analytics.three_p_percent}%"
    )
    insights.append (
        f"Three Pointers Attempted: {game.away_analytics.three_pa} threes"
    )
    insights.append (
        f"Three Pointers Made: {game.away_analytics.three_pm} threes"
    )
    insights.append (
        f"Turnovers: {game.away_analytics.turnover} turnovers"
    )
    insights.append (
        f"Most efficient field goal shooter: {game.away_analytics.most_efficient_fg_player}"
    )
    insights.append (
        f"  {game.away_analytics.most_efficient_fg}% on {game.away_analytics.most_efficient_fgm} of {game.away_analytics.most_efficient_fga} shots" 
    )
    insights.append (
        f"Most efficient three point shooter: {game.away_analytics.most_efficient_3p_player}"
    )
    insights.append (
        f"  {game.away_analytics.most_efficient_3p}% on {game.away_analytics.most_efficient_3pm} of {game.away_analytics.most_efficient_3pa} threes" 
    )
    insights.append (
        f"Least efficient field goal shooter: {game.away_analytics.least_efficient_fg_player}"
    )
    insights.append (
        f"  {game.away_analytics.least_efficient_fg}% on {game.away_analytics.least_efficient_fgm} of {game.away_analytics.least_efficient_fga} shots" 
    )
    insights.append (
        f"Least efficient three point shooter: {game.away_analytics.least_efficient_3p_player}"
    )
    insights.append (
        f"  {game.away_analytics.least_efficient_3p}% on {game.away_analytics.least_efficient_3pm} of {game.away_analytics.least_efficient_3pa} threes" 
    )
    insights.append (
        f"Least impactful player based on points was {game.away_analytics.least_efficient_points_player} who scored at a rate of {game.away_analytics.least_efficient_points} points per minute"
    )





    return insights