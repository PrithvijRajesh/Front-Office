# Nightly email digest with game summaries and links to advanced stats.

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from agent.decision import evaluate_nba_game
from agent.summarizer import summarize_game
from config import load_league_config
from fetchers.nba_data import SUPPORTED_LEAGUES, fetch_all_games_for_leagues
from preferences.learning import is_personalization_active


def espn_game_link(event_id, league="nba"):
    return f"https://www.espn.com/{league}/game/_/gameId/{event_id}"


def advanced_stats_link(event_id):
    base = os.environ.get("APP_BASE_URL", "").strip().rstrip("/")
    if base:
        return f"{base}/stats?game={event_id}"
    return None


def build_digest_body(games_by_league=None, leagues=SUPPORTED_LEAGUES):
    if games_by_league is None:
        games_by_league = {}
        for league in leagues:
            from fetchers.nba_data import fetch_all_games

            games_by_league[league] = fetch_all_games(league=league)

    lines = [
        "Front Office — nightly summary (NBA & WNBA)",
        "",
    ]

    total_shown = 0
    for league in leagues:
        games = games_by_league.get(league, [])
        config = load_league_config(league)
        personalized = is_personalization_active(league)
        label = league.upper()

        lines.append(f"========== {label} ==========")
        if personalized:
            lines.append("Filtered to your learned preferences for this league.")
        else:
            lines.append("Showing notable finished games.")
        lines.append("")

        shown = 0
        for game in games:
            important, reasons = evaluate_nba_game(game, config)
            if personalized and not important:
                continue

            shown += 1
            total_shown += 1
            lines.append(f"{shown}. {game.away_team} @ {game.home_team}")
            lines.append(f"   Final: {game.away_team_score} - {game.home_team_score}")
            if important:
                lines.append(f"   {summarize_game(game, reasons)}")
            else:
                lines.append("   Summary: standard game night.")
            link = advanced_stats_link(game.event_id)
            if link:
                lines.append(f"   View advanced stats: {link}")
            lines.append(f"   ESPN box score: {espn_game_link(game.event_id, game.league)}")
            lines.append("")

        if shown == 0:
            lines.append(f"No {label} games matched tonight.")
            lines.append("")

    if total_shown == 0:
        lines.append("No games matched your preferences tonight.")
    else:
        lines.append(
            "Open the app during 11:59 PM – 12:10 AM and view advanced stats "
            "to refine NBA and WNBA favorites separately."
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
        all_games = fetch_all_games_for_leagues()
        games_by_league = {}
        for game in all_games:
            games_by_league.setdefault(game.league, []).append(game)
        body = build_digest_body(games_by_league)
    else:
        games_by_league = {}
        for game in games:
            games_by_league.setdefault(game.league, []).append(game)
        body = build_digest_body(games_by_league)

    subject = "NBA & WNBA nightly summary — Front Office"

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
