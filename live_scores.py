import http.client
import json

conn = http.client.HTTPSConnection("www.sofascore.com")

payload = ""

# Get these from Insomnia
headers = {

}

conn.request("GET", "/api/v1/sport/football/events/live", payload, headers)

res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))

for event in json_data['events']:
    competition = event['tournament']['name']
    home_team = event['homeTeam']['name']
    away_team = event['awayTeam']['name']
    home_goals = event['homeScore']['current']
    away_goals = event['homeScore']['current']

    print(f"{competition}: {home_team} {home_goals} - {away_goals} {away_team}")