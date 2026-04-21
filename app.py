from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"


def initialize_game():
    session["players"] = {}
    session["scores"] = {}
    session["history"] = []


@app.route("/", methods=["GET", "POST"])
def home():
    if "players" not in session:
        initialize_game()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_player":
            name = request.form.get("name", "").strip()
            initials = request.form.get("initials", "").strip().upper()

            if name and initials:
                players = session["players"]
                scores = session["scores"]

                if initials not in players:
                    players[initials] = name
                    scores[initials] = 0

                    session["players"] = players
                    session["scores"] = scores

        elif action == "submit_round":
            players = session["players"]
            scores = session["scores"]
            history = session["history"]

            round_scores = {}

            for initials in players.keys():
                value = request.form.get(f"turn_{initials}", "").strip().lower()

                if value == "reset":
                    round_scores[initials] = "reset"
                    scores[initials] = 0
                else:
                    try:
                        turn_score = int(value)
                        if turn_score >= 0:
                            round_scores[initials] = turn_score
                            scores[initials] += turn_score
                        else:
                            round_scores[initials] = "invalid"
                    except ValueError:
                        round_scores[initials] = "invalid"

            history.append(round_scores)
            session["scores"] = scores
            session["history"] = history

        elif action == "new_game":
            initialize_game()

        return redirect(url_for("home"))

    return render_template(
        "index.html",
        players=session["players"],
        scores=session["scores"],
        history=session["history"],
    )


if __name__ == "__main__":
    app.run(debug=True)