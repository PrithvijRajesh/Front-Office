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

stats1 = summary["boxscore"]["teams"][0]["statistics"]
stats2 = summary["boxscore"]["teams"][1]["statistics"]
team = summary["boxscore"]["teams"]

with open("nba_data.json", "w") as f:
    json.dump(first_game, f, indent = 2)
with open("nba_summary.json", "w") as f:
    json.dump(filtered_summary, f, indent = 2)

away, home = events[0]["name"].split(" at ")
print(away)
print(home)

if team[0]["team"]["displayName"] == away:
    awayFGM, awayFGA = stats1[0]["displayValue"].split("-")
    awayFGP = int(awayFGM) / int(awayFGA) * 100
    awayTPM, awayTPA = stats1[2]["displayValue"].split("-")
    awayTPP = int(awayTPM) / int(awayTPA) * 100
    homeFGM, homeFGA = stats2[0]["displayValue"].split("-")
    homeFGP = int(homeFGM) / int(homeFGA) * 100
    homeTPM, homeTPA = stats2[2]["displayValue"].split("-")
    homeTPP = int(homeTPM) / int(homeTPA) * 100
else:
    awayFGM, awayFGA = stats2[0]["displayValue"].split("-")
    awayFGP = int(awayFGM) / int(awayFGA) * 100
    awayTPM, awayTPA = stats2[2]["displayValue"].split("-")
    awayTPP = int(awayTPM) / int(awayTPA) * 100
    homeFGM, homeFGA = stats1[0]["displayValue"].split("-")
    homeFGP = int(homeFGM) / int(homeFGA) * 100
    homeTPM, homeTPA = stats1[2]["displayValue"].split("-")
    homeTPP = int(homeTPM) / int(homeTPA) * 100
print(away, awayFGM, awayFGA, awayFGP, awayTPM, awayTPA, awayTPP)
print(home, homeFGM, homeFGA, homeFGP, homeTPM, homeTPA, homeTPP)