from .models import *
from bs4 import BeautifulSoup
import requests
import json
from rich.progress import track


def get_csrf_token(league: League, url: str) -> str:
    r = league.session.get(league.base_url + url)  
    abort_if_badocde(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    idx = r.text.index("'csrfNonce': \"") + 14
    csrf = r.text[idx:idx + CSRF_TOKEN_LEN]
    return csrf


def get_nonce(league: League, url: str) -> str:
    r = league.session.get(league.base_url + url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find('input', {'id': 'nonce'})
    if len(result.attrs['value']) != NONCE_LEN:
        print(f'[!] Invalid NONCE number for league {league["name"]}')
        exit(0)
    return result.attrs['value']


def login_admin(league: League) -> bool:
    r = league.session.post(league.base_url + '/login', data={'name': league.get_admin_name(), 'password': league.get_admin_password(), 'nonce': league.nonce, '_submit': 'Submit'})
    if abort_if_badocde(r):
        return False
    return True


def login_league(league_name: str) -> League:
    league = None
    with open('leagues.json', 'r') as jdata:
        league_json = json.loads(jdata.read())
        league = League(league_name, league_json[league_name]['url'], league_json[league_name]['admin_name'], league_json[league_name]['admin_password'])
        league.nonce = get_nonce(league, '/login')
        
        if login_admin(league):
            print(f'[*] Logged in {league.name} league successfully with handle {league.get_admin_name()}')
        else:
            print(f'[!] Failed to login to {league.name} with handle {league.get_admin_name()}')
    return league


def login_leagues() -> dict:
    leagues = {}
    with open('leagues.json', 'r') as jdata:
        leagues_json = json.loads(jdata.read())
            
        for league_json in [leagues_json[k] for k in leagues_json.keys()]:
            leagues[league_json['name']] = League(league_json['name'], league_json['url'], league_json['admin_name'], league_json['admin_password'])
        
        for league in track([leagues[k] for k in leagues.keys()], description='Logging in...'):
            league.nonce = get_nonce(league, '/login')
            if login_admin(league):
                print(f'[*] Logged in {league.name} league successfully with handle {league.get_admin_name()}')
            else:
                print(f'[!] Failed to login to {league.name} with handle {league.get_admin_name()}')
    return leagues
