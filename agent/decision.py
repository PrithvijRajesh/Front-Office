#Decision making agent to determine what to do with information and what it should care about and send to user


def _all_notable_players(game):
    """Names that might match favorite_players (both teams)."""
    names = []
    for impact in (game.home_impact, game.away_impact):
        names.extend(
            [
                impact.top_scorer,
                impact.top_rebounder,
                impact.top_assister,
                impact.top_stealer,
                impact.top_blocker,
                impact.impact_points_player,
                impact.impact_rebounds_player,
                impact.impact_assists_player,
            ]
        )
    for analytics in (game.home_analytics, game.away_analytics):
        names.extend(
            [
                analytics.most_efficient_fg_player,
                analytics.most_efficient_3p_player,
            ]
        )
    return names


def evaluate_nba_game(game, config):
    """
    Decide whether an NBA game is important to the user.

    Returns:
        (bool, list[str]) -> (is_important, reasons)
    """
    reasons = []

    # Rule 1: Clutch games are important
    if game.clutch_game:
        reasons.append("Clutch game")

    # Rule 2: Comeback games are important
    if game.comeback_game:
        reasons.append("Comeback game")

    # Rule 3: Game with high total scores
    if game.total_score > config.high_total:
        reasons.append(f"High total score: {game.total_score}")

    # Rule 4: Games where favorite team is playing
    playing = {game.home_team, game.away_team}
    fav_teams = set(config.favorite_teams)
    matched_teams = playing & fav_teams
    if matched_teams:
        reasons.append(f"Favorite team playing: {', '.join(sorted(matched_teams))}")

    # Rule 5: Either team's leading scorer cleared the high-points bar
    for team_name, impact in (
        (game.home_team, game.home_impact),
        (game.away_team, game.away_impact),
    ):
        if impact.top_points > config.high_points:
            reasons.append(
                f"High scoring ({team_name}): {impact.top_scorer} ({impact.top_points} pts)"
            )

    # Rule 6: Favorite player appears in notable roles (either team)
    notable = set(_all_notable_players(game))
    for player in config.favorite_players:
        if player in notable:
            reasons.append(f"Favorite player featured: {player}")

    # Rule 7: Post Season games
    if game.post_season:
        reasons.append("Post Season game")

    # Rule 8: Post Season Impact games
    if game.post_season_impact:
        reasons.append("Game has post season implications")

    # Final decision
    is_important = len(reasons) > 0
    return is_important, reasons
