import json

with open('20241028-live-scores-sample.json') as f:
    json_data = json.load(f)

for event in json_data['events']:
    competition = event['tournament']['name']
    home_team = event['homeTeam']['name']
    away_team = event['awayTeam']['name']
    home_goals = event['homeScore']['current']
    away_goals = event['homeScore']['current']

    print(f"{competition}: {home_team} {home_goals} - {away_goals} {away_team}")