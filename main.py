from flask import Flask, render_template, request, redirect, url_for
import ast
app = Flask(__name__)

options = [
    {'name': 'League Of Legends', 'image': 'leagueOfLegends.png','banner':'LoLbanner.png'},
    {'name': 'Valorant', 'image': 'valorant.png','banner':'ValorantBanner.png'},
    {'name': 'Counter-Strike', 'image': 'CounterStrike.png','banner':'CSGOBanner.png'},
    {'name': 'Rocket League', 'image': 'RocketLeague.png','banner':'RocketLeagueHeader.png'},
    {'name': 'Fortnite', 'image': 'Fortnite.png','banner':'FortniteBanner.png'}
]    
number_of_ranks = 5
remaining_ranks = list(range(1, number_of_ranks + 1))
rankings = []
rankings2 = {1: "", 2: "", 3: "", 4: "", 5: ""}
rankings3 = {1: "white.jpg", 2: "white.jpg", 3: "white.jpg", 4: "white.jpg", 5: "white.jpg"}


@app.route('/')
def previous():
    reset()
    # Render the previous page template
    return render_template('main.html')
@app.route('/blindrank')
def index():
    remaining_options = [option for option in options if option['name'] not in [r[1] for r in rankings]]
    if remaining_options:
        next_option = remaining_options[0]
        return render_template('rank.html', option=next_option, remaining_options=remaining_options,rankings3=rankings3,
                               remaining_ranks=remaining_ranks, rankings2=rankings2, clicked_rank=request.args.get('rank'))
    else:
        ranked_options = [ranked_option for _, ranked_option in sorted(rankings)]
        return render_template('rank.html', option="Ranking complete", rankings=ranked_options, rankings2=rankings2,rankings3=rankings3,
                               remaining_options=[], clicked_rank=None)


@app.route('/rank', methods=['POST'])
def rank():
    ranked_option = request.form['ranked_option']
    rank = request.form['rank']
    remaining_ranks.remove(int(rank))
    rankings.append((rank, ast.literal_eval(ranked_option)["name"]))
    rankings2[int(rank)] = str(ast.literal_eval(ranked_option)["name"])
    rankings3[int(rank)] = str(ast.literal_eval(ranked_option)["banner"])
    print(rankings3)

    return redirect(url_for('index', rank=rank))


@app.route('/reset', methods=['POST'])
def reset():
    global rankings
    rankings = []
    global remaining_ranks
    global rankings2
    global rankings3
    rankings3 = {1: "white.jpg", 2: "white.jpg", 3: "white.jpg", 4: "white.jpg", 5: "white.jpg"}
    rankings2 = {1: "", 2: "", 3: "", 4: "", 5: ""}
    remaining_ranks = list(range(1, number_of_ranks + 1))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
