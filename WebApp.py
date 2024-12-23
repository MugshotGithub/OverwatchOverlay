from flask import Flask, render_template, request, make_response

app = Flask(__name__)

team1 = {
    "name": "Team 1",
    "image": "teams/None.png",
    "score": 0,
    "ban": "bans/None.png"
}

team2 = {
    "name": "Team 2",
    "image": "teams/None.png",
    "score": 0,
    "ban": "bans/None.png"
}


@app.route('/')
def index():
    return render_template("base.html", team1=team1, team2=team2)

@app.route('/api/updateName', methods=['POST'])
def updateName():
    if int(request.form.get("teamNumber")) == 1:
        team = team1
    else:
        team = team2

    team["name"] = request.form.get("teamName")

    return make_response("OK", 200)

@app.route('/api/updateScore', methods=['POST'])
def updateScore():
    if int(request.form.get("teamNumber")) == 1:
        team = team1
    else:
        team = team2

    team["score"] = int(request.form.get("teamScore"))

    return make_response("OK", 200)

@app.route('/api/updateBwaa', methods=['POST'])
def updateBwaa():
    if int(request.form.get("teamNumber")) == 1:
        team = team1
    else:
        team = team2

    team["image"] = f"teams/{request.form.get("teamBwaa")}.png"
    print(team["image"])

    return make_response("OK", 200)
@app.route('/api/updateBanned', methods=['POST'])
def updateBan():
    if int(request.form.get("teamNumber")) == 1:
        team = team1
    else:
        team = team2

    team["ban"] = f"bans/{request.form.get("teamBan")}.png"

    return make_response("OK", 200)

@app.route('/api/swapTeams', methods=['GET'])
def swapTeams():
    global team1
    global team2
    team1, team2 = team2, team1
    return make_response("OK", 200)

if __name__ == "__main__":
    app.run(debug=True)
