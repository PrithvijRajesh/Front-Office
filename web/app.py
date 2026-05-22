"""
Browser UI for Front Office. By default only open 11:59 PM – 12:10 AM.

Run manually (any time, for testing):
  set SKIP_TIME_WINDOW=1
  python -m web.app

Nightly (email + 11-minute window):
  python scripts/nightly_window.py
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, render_template_string, request

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from agent.analysis import analyze_nba_game
from agent.decision import evaluate_nba_game
from agent.summarizer import summarize_game
from config import load_league_config
from fetchers.nba_data import fetch_all_games_for_leagues
from preferences.learning import is_personalization_active, preference_summary
from preferences.store import record_advanced_stat_view

app = Flask(__name__)

_games_by_id = {}
_games_loaded_at = None


def is_app_window_open():
    if os.environ.get("SKIP_TIME_WINDOW") == "1":
        return True
    now = datetime.now()
    if now.hour == 23 and now.minute >= 59:
        return True
    if now.hour == 0 and now.minute <= 10:
        return True
    return False


def require_window():
    if not is_app_window_open():
        abort(
            403,
            description=(
                "Front Office is only available from 11:59 PM to 12:10 AM. "
                "Check your email during that window, or run with "
                "SKIP_TIME_WINDOW=1 for local testing."
            ),
        )


def load_games():
    global _games_by_id, _games_loaded_at
    games = fetch_all_games_for_leagues()
    _games_by_id = {g.event_id: g for g in games if g.event_id}
    _games_loaded_at = datetime.now()
    return list(_games_by_id.values())


def get_games():
    if not _games_by_id:
        return load_games()
    return list(_games_by_id.values())


def should_show_game(game):
    config = load_league_config(game.league)
    important, _ = evaluate_nba_game(game, config)
    if is_personalization_active(game.league):
        return important
    return True


HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>NBA Front Office</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
    h1 { font-size: 1.5rem; }
    .game { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
    a.button { display: inline-block; margin-top: 0.5rem; padding: 0.5rem 1rem;
               background: #1d428a; color: white; text-decoration: none; border-radius: 6px; }
    .meta { color: #555; font-size: 0.9rem; }
    .prefs { background: #f4f4f4; padding: 0.75rem; border-radius: 6px; font-size: 0.85rem; }
  </style>
</head>
<body>
  <h1>NBA Front Office</h1>
  <p class="meta">Available 11:59 PM – 12:10 AM · {{ games|length }} game(s) (NBA & WNBA)</p>
  <pre class="prefs">{{ prefs }}</pre>
  {% for item in items %}
  <div class="game">
    <h2>[{{ item.game.league|upper }}] {{ item.game.away_team }} @ {{ item.game.home_team }}</h2>
    <p>Final: {{ item.game.away_team_score }} – {{ item.game.home_team_score }}</p>
    {% if item.summary %}<p>{{ item.summary }}</p>{% endif %}
    <a class="button" href="/stats?game={{ item.game.event_id }}">View advanced stats</a>
  </div>
  {% else %}
  <p>No games to show right now.</p>
  {% endfor %}
</body>
</html>
"""

STATS_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
    li { margin: 0.35rem 0; }
    a { color: #1d428a; }
  </style>
</head>
<body>
  <p><a href="/">← All games</a></p>
  <h1>{{ title }}</h1>
  <p>Final: {{ away_score }} – {{ home_score }}</p>
  <ul>
  {% for line in lines %}
    <li>{{ line }}</li>
  {% endfor %}
  </ul>
</body>
</html>
"""

CLOSED_HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Front Office — closed</title></head>
<body style="font-family: system-ui; max-width: 520px; margin: 3rem auto; text-align: center;">
  <h1>Not available right now</h1>
  <p>Front Office opens <strong>11:59 PM – 12:10 AM</strong> each night.</p>
  <p>Your nightly email arrives at 11:59 PM with links that work during this window.</p>
</body>
</html>
"""


@app.errorhandler(403)
def closed_handler(e):
    return render_template_string(CLOSED_HTML), 403


@app.before_request
def check_window():
    if request.endpoint == "static":
        return
    require_window()


@app.route("/")
def home():
    items = []
    for game in get_games():
        if not should_show_game(game):
            continue
        config = load_league_config(game.league)
        important, reasons = evaluate_nba_game(game, config)
        summary = summarize_game(game, reasons) if important else ""
        items.append({"game": game, "summary": summary})

    return render_template_string(
        HOME_HTML,
        items=items,
        games=get_games(),
        prefs=preference_summary(),
    )


@app.route("/stats")
def stats():
    event_id = request.args.get("game", "")
    game = _games_by_id.get(event_id)
    if not game:
        load_games()
        game = _games_by_id.get(event_id)
    if not game:
        abort(404, description="Game not found.")

    record_advanced_stat_view(game)
    lines = analyze_nba_game(game)
    title = f"[{game.league.upper()}] {game.away_team} @ {game.home_team}"

    return render_template_string(
        STATS_HTML,
        title=title,
        away_score=game.away_team_score,
        home_score=game.home_team_score,
        lines=lines,
    )


def main():
    port = int(os.environ.get("PORT", "8000"))
    load_games()
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
