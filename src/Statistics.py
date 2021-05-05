import csv
import requests
import json
from rich.progress import track
import numpy
import pandas

from config import *
from core.models import *
from core.funcs import *


# Requires filled leagues.json, users.csv and teams.csv\
# Please don't forget that `leagues` argument must contain only leagues which you are logged in
def generate_table(league: League = None, league_name: str = "", save_as_file: bool = False, html_table: bool = False):
    if not save_as_file and not html_table:
        print("[!] No mode provided for table generator")
        return
    
    if not league:
        league = login_league(league_name)

    challenges = {}
    challenges_default = {}
    
    r = league.get('/api/v1/challenges')
    challenges_data = r.json()['data']
    for challenge_data in track(challenges_data, description='Getting list of challenges'):
        challenges[challenge_data['id']] = Challenge(challenge_data['name'], challenge_data['type'], challenge_data['category'], sid=challenge_data['id'])
        challenges_default[challenge_data['id']] = False
    print('[*] List of challenges retrieved')
    

    r = league.get('/api/v1/teams')
    teams = r.json()['data']
    for i in track(range(len(teams)), description='Getting list of teams...'):
        teams[i] = Team(teams[i]['name'], teams[i]['email'], sid=teams[i]['id'])
        teams[i].solves = challenges_default.copy()
        teams[i].fails = challenges_default.copy()
        
        # firstly we get fails and then solves because /api/v1/fails returns all fails even if team succeeded 
        r = league.get(f'/api/v1/teams/{teams[i].sid}/fails')
        for challenge in r.json()['data']:
            teams[i].fails[challenge['challenge_id']] = True

        r = league.get(f'/api/v1/teams/{teams[i].sid}/solves')
        for challenge in r.json()['data']:
            teams[i].solves[challenge['challenge_id']] = True

    print('[*] List of teams retrieved')

    if save_as_file:
        csv_columns = ['Teams/Tasks'] + [challenges[ch].name for ch in challenges.keys()]
        dict_data = [None for i in range(len(teams))]
        index = 0
        
        for team in track(teams, description='Generating table...'):
            dict_data[index] = {'Teams/Tasks': team.name}
            
            for ch_id in team.fails.keys():
                if team.fails[ch_id]:
                    dict_data[index][challenges[ch_id].name] = '-'
                else:
                    dict_data[index][challenges[ch_id].name] = '.'
            for ch_id in team.solves.keys():
                if team.solves[ch_id]:
                    dict_data[index][challenges[ch_id].name] = '+' 
            index += 1
        
        with open(f'tasks_per_team_{league.name}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in track(dict_data, description='Writing data to csv file...'):
                writer.writerow(data)
        print(f'[*] CSV-table for {league.name} league created')
    if html_table:
        t_challenges = [challenges[ch] for ch in challenges.keys()]
        t_teams = [team.name for team in teams]
        t_solves = [[str(i+j) for j in range(len(challenges.keys()))] for i in range(len(teams))]
        
        for i in range(len(t_teams)):
            for j in range(len(t_challenges)):
                if teams[i].fails[t_challenges[j].sid]:
                    t_solves[i][j] = '-'
                else:
                    t_solves[i][j] = '.'
                if teams[i].solves[t_challenges[j].sid]:
                    t_solves[i][j] = '+'

        t_challenges = [ch.name for ch in t_challenges]

        t_solves = numpy.array(t_solves)
        t_df = pandas.DataFrame(t_solves, index=t_teams, columns=t_challenges)
        print(f'[*] Array-based table for {league.name} league created')
        return t_df


if __name__ == '__main__':
    generate_table(league_name='junior', save_as_file=True)
