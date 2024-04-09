from flask import Flask, render_template, request, redirect, url_for, session
import ast
from utils import *
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'asdasdasdas'  # Provide a secret key for session encryption
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'asd'
app.config['SESSION_COOKIE_NAME'] = 'aasasd'
Session(app)
# Sample list of categories
categories = [
    {'name': 'Gaming', 'image': './static/game-console.png'},
    {'name': 'Technology', 'image': './static/technology.png'},
    {'name': 'Sports', 'image': './static/sports.png'},
    {'name': 'Music', 'image': './static/music.png'},
    # Add more categories as needed
]
number_of_ranks = 5

@app.route('/')
def previous():
    session.clear()  # Clear session data on each new request
    return render_template('main.html', categories=categories)

@app.route('/blindrank')
def index():
    category = request.args.get('categories')
    if category:
        options = getOptions(category)
        session['options'] = options  # Store options in session
    else:
        options = session.get('options', [])

    rankings = session.get('rankings', [])
    remaining_ranks = session.get('remaining_ranks', list(range(1, number_of_ranks + 1)))
    rankings2 = session.get('rankings2', {1: "", 2: "", 3: "", 4: "", 5: ""})
    rankings3 = session.get('rankings3', {1: "white.jpg", 2: "white.jpg", 3: "white.jpg", 4: "white.jpg", 5: "white.jpg"})

    remaining_options = [option for option in options if option['name'] not in [r[1] for r in rankings]]

    if remaining_options:
        next_option = remaining_options[0]
        return render_template('rank.html', option=next_option, remaining_options=remaining_options,
                               rankings3=rankings3, remaining_ranks=remaining_ranks,
                               rankings2=rankings2, clicked_rank=request.args.get('rank'))
    else:
        ranked_options = [ranked_option for _, ranked_option in sorted(rankings)]
        return render_template('rank.html', option="Ranking complete", rankings=ranked_options,
                               rankings2=rankings2, rankings3=rankings3,
                               remaining_options=[], clicked_rank=None)

@app.route('/rank', methods=['POST'])
def rank():
    ranked_option = request.form['ranked_option']
    rank = request.form['rank']

    # Retrieve session data
    rankings = session.get('rankings', [])
    remaining_ranks = session.get('remaining_ranks', list(range(1, number_of_ranks + 1)))
    rankings2 = session.get('rankings2', {1: "", 2: "", 3: "", 4: "", 5: ""})
    rankings3 = session.get('rankings3', {1: "white.jpg", 2: "white.jpg", 3: "white.jpg", 4: "white.jpg", 5: "white.jpg"})

    remaining_ranks.remove(int(rank))
    rankings.append((rank, ast.literal_eval(ranked_option)["name"]))
    print(str(ast.literal_eval(ranked_option)["name"]))
    rankings2[int(rank)] = str(ast.literal_eval(ranked_option)["name"])
    rankings3[int(rank)] = str(ast.literal_eval(ranked_option)["banner"])

    # Update session data
    session['remaining_ranks'] = remaining_ranks
    session['rankings'] = rankings
    session['rankings2'] = rankings2
    session['rankings2'] = {int(k): v for k, v in  session['rankings2'].items()}
    session['rankings3'] = rankings3
    session['rankings3'] = {int(k): v for k, v in  session['rankings3'].items()}
    print(session["rankings2"])
    return redirect(url_for('index', rank=rank))

@app.route('/reset', methods=['POST'])
def reset():
    session['rankings'] = []
    session['remaining_ranks'] = list(range(1, number_of_ranks + 1))
    session['rankings2'] = {1: "", 2: "", 3: "", 4: "", 5: ""}
    session['rankings2'] = {int(k): v for k, v in  session['rankings2'].items()}
    session['rankings3'] = {1: "white.jpg", 2: "white.jpg", 3: "white.jpg", 4: "white.jpg", 5: "white.jpg"}
    session['rankings3'] = {int(k): v for k, v in  session['rankings3'].items()}
    return redirect(url_for('index',remaining_ranks=session['remaining_ranks']))

if __name__ == '__main__':
    app.run(debug=True)
