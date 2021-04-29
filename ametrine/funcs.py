from .classes import *
from bs4 import BeautifulSoup
import requests


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
