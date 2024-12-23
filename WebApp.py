from flask import Flask
from flask import render_template

# from flask import request


# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():

    team1 = {
        "name": "Zeta",
        "image": "teams/Zeta.png",
        "score": 0,
        "ban": "bans/brig.png"
    }

    team2 = {
        "name": "Crazy Raccoon",
        "image": "teams/CrazyRaccoon.png",
        "score": 0,
        "ban": "bans/mauga.png"
    }

    return render_template("base.html", team1=team1, team2=team2)

app.run(debug=True)