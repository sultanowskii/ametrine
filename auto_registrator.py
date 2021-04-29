import csv
import requests
import json

from config import *
from ametrine.classes import *
from ametrine.funcs import *


def main():    
    leagues = {}

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

    # Team registration
    print('======Teams registration======')
    with open('teams.csv', 'r') as data:
        teams = csv.DictReader(data)
        for team in teams:
            if team['league'] not in leagues.keys():
                print(f'[!] No correct league provided for team {team["name"]}, skipped')
                continue
            league = leagues[team['league']]
            json_team = {
                'name': team['name'],
                'email': team['email'],
                'password': team['password'],
                'hidden': False,
                'banned': False,
                'fields': []
            }

            csrf = get_csrf_token(league, '/admin/teams/new')
            r = league.post('/api/v1/teams', json=json_team, headers={'Content-Type': 'application/json', 'CSRF-Token': csrf})
            print(f'[.] Team {team["name"]} registered successfully to {team["league"]} league')
            league.teams[team['name']] = Team(team['name'], team['email'], team['password'], r.json()['data']['id'])

    print('======Users registration======')

    # User registration + adding them to teams
    with open('users.csv', 'r') as data:
        users = csv.DictReader(data)
        for user in users:
            json_user = {
                'name': user['name'],
                'email': user['email'],
                'password': user['password'],
                'type': 'user',
                'verified': False,
                'hidden': False,
                'banned': False,
                'fields': []
            }

            if user['league'] not in leagues.keys():
                print(f'[!] No correct league provided for user {user["name"]}, skipped')
                continue

            league = leagues[user['league']]
            
            # Register user with CSRF token on page (without it we get 403 from server)
            csrf = get_csrf_token(league, '/admin/users/new')
            r = league.post('/api/v1/users', json=json_user, headers={'Content-Type': 'application/json', 'CSRF-Token': csrf})
            print(f'[.] User {user["name"]} registered successfully to {user["league"]} league')
            user_id = r.json()['data']['id']
            team_id = league.teams[user['team']].sid

            # Add user to team
            csrf = get_csrf_token(league, f'/admin/teams/{team_id}')
            r = league.post(f'/api/v1/teams/{team_id}/members', json={'user_id': user_id}, headers={'Content-Type': 'application/json', 'CSRF-Token': csrf})
            print(f'[.] User {user["name"]} added successfully to {user["team"]} team in {user["league"]} league')
            league.teams[user['team']].users[user['name']] = User(user['name'], user['email'], user['password'], user_id)

if __name__ == '__main__':
    main()
