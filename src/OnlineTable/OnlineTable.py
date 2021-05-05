from flask import Flask, render_template, request, redirect, url_for, flash, make_response

# importing from parent package
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from Statistics import generate_table
from core.funcs import login_leagues

NO_ATTEMPTS_COLOR = '#6c757d'
SOLVED_COLOR = '#28a745'
NOT_SOLVED_COLOR = '#dc3545'
HOST = '0.0.0.0'
PORT = 5000

leagues = login_leagues()
app = Flask(__name__)


def generate_list(data: list):
    result = '<ul>'
    for el in data:
        result += f'\n\t<li><a href="/{el}/attempts">{el} league</a></li>'
    result += '</ul>'
    return result


# list of all leagues
@app.route('/', methods=['GET'])
def leagues_list():
    llist = generate_list(leagues.keys())
    return render_template('leagues.html', leagues_list=llist)


# table 'teams-attempts'
@app.route('/<league_name>/attempts')
def league_table(league_name):
    if league_name not in leagues.keys():
        return f"League {league} not found", 404
    df = generate_table(league=leagues[league_name], html_table=True).to_html()
    df = df.replace('<td>.', f'<td bgcolor={NO_ATTEMPTS_COLOR}>')
    df = df.replace(f'<td>+', f'<td bgcolor={SOLVED_COLOR}>')
    df = df.replace(f'<td>-', f'<td bgcolor={NOT_SOLVED_COLOR}>')
    df = df.replace('text-align: right', 'text-align: left')
    df = df.replace('<table border="1" class="dataframe">', '<table border="1" width="94%">')
    return render_template('attempts.html', ltable=df, lname=league_name)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
