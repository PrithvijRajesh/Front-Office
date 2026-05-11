# Front-Office

A small Python project for learning how to build a **sports-focused AI-style agent**: fetch or mock game data, apply **preference-based rules** to decide what matters to you, and eventually summarize news and scores.

Current focus: **NBA** (starting with fake game summaries, then real APIs later).

## Requirements

- Python 3.10+ recommended

## Run

From the project root (`Front-Office`):

```bash
python3 main.py
```

This loads fake games from `agent/tests/nba_game_test_data.py`, applies rules in `agent/decision.py`, and prints whether each game is “important” and why.

## Layout

| Path | Role |
|------|------|
| `main.py` | Entry point: wires config + fake data + decision logic |
| `config.py` | User preferences (`NBAConfig` dataclass) |
| `models/nba_games.py` | Data shapes (`NBAGameSummary`, team stats, etc.) |
| `agent/decision.py` | Rule engine: what counts as important |
| `agent/tests/nba_game_test_data.py` | Fake games for testing logic without APIs |

