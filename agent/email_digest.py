# Nightly email digest with game summaries and links to advanced stats.

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from agent.decision import evaluate_nba_game
from agent.summarizer import summarize_game
from config import load_nba_config
from fetchers.nba_data import fetch_all_games
from preferences.learning import is_personalization_active


def espn_game_link(event_id):
    """Public box score / game page (always works in a browser)."""
    return f"https://www.espn.com/nba/game/_/gameId/{event_id}"


def advanced_stats_link(event_id):
    """Local app during 11:59–12:10 AM, or ESPN if APP_BASE_URL is unset."""
    base = os.environ.get("APP_BASE_URL", "").strip().rstrip("/")
    if base:
        return f"{base}/stats?game={event_id}"
    return espn_game_link(event_id)


def build_digest_body(games, config):
    personalized = is_personalization_active()
    lines = [
        "NBA Front Office — nightly summary",
        "",
    ]

    if personalized:
        lines.append(
            "Showing games matched to your learned preferences "
            "(teams/players you often view advanced stats for)."
        )
    else:
        lines.append("Showing notable games from today's scoreboard.")
    lines.append("")

    shown = 0
    for game in games:
        important, reasons = evaluate_nba_game(game, config)
        if personalized and not important:
            continue

        shown += 1
        lines.append(f"{shown}. {game.away_team} @ {game.home_team}")
        lines.append(f"   Final: {game.away_team_score} - {game.home_team_score}")
        if important:
            lines.append(f"   {summarize_game(game, reasons)}")
        else:
            lines.append("   Summary: standard game night.")
        lines.append(f"   View advanced stats: {advanced_stats_link(game.event_id)}")
        lines.append(f"   ESPN box score: {espn_game_link(game.event_id)}")
        lines.append("")

    if shown == 0:
        lines.append("No games matched your preferences tonight.")
    else:
        lines.append(
            "In the app, open a game and choose to view advanced stats — "
            "that helps us learn your favorite teams and players."
        )

    return "\n".join(lines)


def send_nightly_email(games=None, config=None):
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")
    email_from = os.environ.get("EMAIL_FROM", smtp_user)

    if not all([smtp_host, smtp_user, smtp_password, email_to]):
        raise RuntimeError(
            "Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD, and EMAIL_TO in .env to send email."
        )

    if games is None:
        games = fetch_all_games()
    if config is None:
        config = load_nba_config()

    body = build_digest_body(games, config)
    subject = "NBA nightly summary — Front Office"

    message = MIMEMultipart()
    message["From"] = email_from
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    port = int(os.environ.get("SMTP_PORT", "587"))
    with smtplib.SMTP(smtp_host, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, [email_to], message.as_string())

    return body
