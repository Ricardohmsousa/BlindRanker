from flask import Flask, render_template, request, redirect, url_for, session
import ast
from utils import getOptions
from flask_session import Session
import uuid  # for generating unique tab identifiers

app = Flask(__name__)
app.secret_key = 'asdasdasdas'  # Provide a secret key for session encryption
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'asd'
app.config['SESSION_COOKIE_NAME'] = 'aasasd'
Session(app)

# Dictionary to store session data per tab
tab_sessions = {}

# Sample list of categories
categories = [
    {'name': 'Gaming', 'image': './static/game-console.png'},
    {'name': 'Technology', 'image': './static/technology.png'},
    {'name': 'Sports', 'image': './static/sports.png'},
    {'name': 'Music', 'image': './static/music.png'},
    # Add more categories as needed
]
number_of_ranks = 5

def generate_tab_id():
    return str(uuid.uuid4())

@app.route('/')
def previous():
    tab_id = generate_tab_id()
    tab_sessions[tab_id] = {'rankings': [], 'remaining_ranks': list(range(1, number_of_ranks + 1)),
                            'rankings2': {i: "" for i in range(1, number_of_ranks + 1)},
                            'rankings3': {i: "white.jpg" for i in range(1, number_of_ranks + 1)}}
    return render_template('main.html', categories=categories, tab_id=tab_id)

@app.route('/blindrank')
def index():
    tab_id = request.args.get('tab_id')
    session_data = tab_sessions.get(tab_id, {})
    options = session_data.get('options', [])
    category = request.args.get('categories')
    if category:
        options = getOptions(category)
        session_data['options'] = options  # Store options in session

    rankings = session_data.get('rankings', [])
    remaining_ranks = session_data.get('remaining_ranks', list(range(1, number_of_ranks + 1)))
    rankings2 = session_data.get('rankings2', {i: "" for i in range(1, number_of_ranks + 1)})
    rankings3 = session_data.get('rankings3', {i: "white.jpg" for i in range(1, number_of_ranks + 1)})
    print(rankings)
    remaining_options = [option for option in options if option['name'] not in [r[1] for r in rankings]]
    print(remaining_options)
    if remaining_options:
        next_option = remaining_options[0]
        print(next_option)
        return render_template('rank.html', option=next_option, remaining_options=remaining_options,
                               rankings3=rankings3, remaining_ranks=remaining_ranks,category=category,
                               rankings2=rankings2, clicked_rank=request.args.get('rank'), tab_id=tab_id)
    else:
        ranked_options = [ranked_option for _, ranked_option in sorted(rankings)]
        return render_template('rank.html', option="Ranking complete", rankings=ranked_options,
                               rankings2=rankings2, rankings3=rankings3,
                               remaining_options=[], clicked_rank=None, tab_id=tab_id)

@app.route('/rank', methods=['POST'])
def rank():
    tab_id = request.form['tab_id']
    ranked_option = request.form['ranked_option']
    rank = request.form['rank']

    session_data = tab_sessions.get(tab_id, {})
    rankings = session_data.get('rankings', [])
    remaining_ranks = session_data.get('remaining_ranks', list(range(1, number_of_ranks + 1)))
    rankings2 = session_data.get('rankings2', {i: "" for i in range(1, number_of_ranks + 1)})
    rankings3 = session_data.get('rankings3', {i: "white.jpg" for i in range(1, number_of_ranks + 1)})

    remaining_ranks.remove(int(rank))
    rankings.append((rank, ast.literal_eval(ranked_option)["name"]))
    rankings2[int(rank)] = str(ast.literal_eval(ranked_option)["name"])
    rankings3[int(rank)] = str(ast.literal_eval(ranked_option)["banner"])

    session_data['remaining_ranks'] = remaining_ranks
    session_data['rankings'] = rankings
    session_data['rankings2'] = rankings2
    session_data['rankings3'] = rankings3
    tab_sessions[tab_id] = session_data

    return redirect(url_for('index', rank=rank, tab_id=tab_id))

@app.route('/reset', methods=['POST'])
def reset():
    tab_id = generate_tab_id()
    category = request.form['category']
    tab_sessions[tab_id] = {'rankings': [], 'remaining_ranks': list(range(1, number_of_ranks + 1)),
                            'rankings2': {i: "" for i in range(1, number_of_ranks + 1)},
                            'rankings3': {i: "white.jpg" for i in range(1, number_of_ranks + 1)}}
    # Redirect back to the ranking page with the updated session data
    return redirect(url_for('index', tab_id=tab_id,categories=category))

if __name__ == '__main__':
    app.run(debug=True)
