import csv
import requests
import json

from config import *
from ametrine.classes import *
from ametrine.funcs import *

def main():    
    leagues = {}
    challenges = {}

    try:
        with open('leagues.json', 'r') as jdata:
            leagues_json = json.loads(jdata.read())
    except Exception as e:
        print(f'[!] legaues.json is not found or broken. Error:\n{e}')
        return

    for league_json in [leagues_json[k] for k in leagues_json.keys()]:
        leagues[league_json['name']] = League(league_json['name'], league_json['url'], league_json['admin_name'], league_json['admin_password'])

    # Init sessions for each league
    # Get NONCEs for login and some other operations
    # Login to leagues using NONCE
    print('==========Logging in==========')
    for league in [leagues[k] for k in leagues.keys()]:
        league.nonce = get_nonce(league, '/login')
        if login_admin(league):
            print(f'[*] Logged in {league.name} league successfully with handle {league.get_admin_name()}')
        else:
            print(f'[!] Failed to login to {league.name} with handle {league.get_admin_name()}')

    for league in [leagues[k] for k in leagues.keys()]:
        print('=====Getting list of challenges=====')
        r = league.get('/api/v1/challenges')
        challenges_data = r.json()['data']
        solved_challenges_default = {}
        for challenge_data in challenges_data:
            challenges[challenge_data['id']] = Challenge(challenge_data['name'], challenge_data['type'], challenge_data['category'], sid=challenge_data['id'])
            solved_challenges_default[challenge_data['id']] = False
        print('[*] List of challenges retrieved')
        

        print('======Getting list of teams======')
        r = league.get('/api/v1/teams')
        teams = r.json()['data']
        for i in range(len(teams)):
            teams[i] = Team(teams[i]['name'], teams[i]['email'], sid=teams[i]['id'])
            teams[i].challenges = solved_challenges_default.copy()
            r = league.get(f'/api/v1/teams/{teams[i].sid}/solves')
            for challenge in r.json()['data']:
                teams[i].challenges[challenge['challenge_id']] = True
        print("[*] List of teams retrieved")

        print('======Generating table======')
        csv_columns = ['Teams/Tasks'] + [challenges[ch].name for ch in challenges.keys()]
        dict_data = [None for i in range(len(teams))]
        index = 0
        for team in teams:
            dict_data[index] = {'Teams/Tasks': team.name}
            for ch_id in team.challenges.keys():
                dict_data[index][challenges[ch_id].name] = '+' if team.challenges[ch_id] else '-'
            index += 1
        with open(f'tasks_per_team_{league.name}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
        print(f'[*] Table for {league.name} created')

if __name__ == '__main__':
    main()
