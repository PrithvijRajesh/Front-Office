# Front-Office

Sports agent: fetch **NBA & WNBA** games from ESPN, apply **per-league preferences**, summarize games, and learn favorites when you view advanced stats.

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Run

```bash
# NBA + WNBA (default)
python main.py

# One league
python main.py --league nba
python main.py --league wnba

# Web UI (test anytime with time window skipped)
set SKIP_TIME_WINDOW=1
python main.py --serve

# Email preview / send
python main.py --email-preview
python main.py --email
```

## Preferences (`data/user_preferences.json`)

Separate blocks for **nba** and **wnba**:

- `manual_favorite_teams` / `manual_favorite_players`
- `advanced_stat_views` — each time you view advanced stats, that league learns your interests

After 5 views in a league, filtering uses learned favorites for that league only.

Example:

```json
{
  "nba": {
    "manual_favorite_teams": ["Warriors", "Pistons"],
    "manual_favorite_players": [],
    "advanced_stat_views": []
  },
  "wnba": {
    "manual_favorite_teams": ["Liberty"],
    "manual_favorite_players": [],
    "advanced_stat_views": []
  }
}
```

## Fetchers

| File | Role |
|------|------|
| `fetchers/nba_data.py` | ESPN basketball API + mapper (`league="nba"` default) |
| `fetchers/wnba_data.py` | Thin WNBA wrapper (`league="wnba"`) |

Same JSON format; only the URL path changes (`/nba/` vs `/wnba/`).

## Layout

| Path | Role |
|------|------|
| `main.py` | CLI: real games, preference learning |
| `config.py` | Per-league thresholds + `load_league_config()` |
| `preferences/` | Store views & infer favorites per league |
| `web/app.py` | Browser UI 11:59 PM – 12:10 AM |
| `agent/email_digest.py` | Nightly email (NBA + WNBA sections) |
