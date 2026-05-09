#Decision making agent to determine what to do with information and what it should care about and send to user

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

    # Final decision
    is_important = len(reasons) > 0
    return is_important, reasons