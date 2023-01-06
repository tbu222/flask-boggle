from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

@app.route("/")
def homepage():
    """show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore",0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route("/checking-word")
def checking_word():
    """checking valid word"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route("/score", methods=["POST"])
def post_score():
    """update score"""
    score = request.json["score"]
    highscore = session.get("highscore",0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays +1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord= score> highscore)