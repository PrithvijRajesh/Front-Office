#Sports data fetcher to return raw sports results and data#Sports data fetcher to return raw sports results and data

import requests
import json

baseURL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
def fetch_nba_data():
    url = f"{baseURL}/scoreboard"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

data = fetch_nba_data()
events = data["events"]
first_game = events[0]
id = events[0]["id"]

def fetch_summary(event_id: str):
    url = f"{baseURL}/summary?event={event_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


summary = fetch_summary(id)

filtered_summary = {
    "teams": summary["boxscore"]["teams"],
    "players": summary["boxscore"]["players"],
    "plays": summary["plays"],
    "win_probability": summary["winprobability"]
}

with open("nba_data.json", "w") as f:
    json.dump(first_game, f, indent = 2)
with open("nba_summary.json", "w") as f:
    json.dump(filtered_summary, f, indent = 2)