import requests
import csv
import json
from rich.progress import track

from config import *
from core.models import *
from core.funcs import *


# Please don't forget that `leagues` argument must contain only leagues which you are logged in
def register_leagues(leagues: dict = {}) -> dict:
    if not leagues:
        leagues = login_leagues()

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
        for user in track(users, description='User registration...'):
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
    return leagues


if __name__ == '__main__':
    register_leagues()
