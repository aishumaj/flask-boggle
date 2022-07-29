from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    # return with json
    return jsonify(gameId= game_id, board= game.board)


# create another route for /api/score-word
# if not boggle.is_word_in_word_list => return "not-word"
# if not boggle.check_word_on_board => return "not-on-board"
# else => play_and_score_word => return "ok"
@app.post("/api/score-word")
def score_word():
    breakpoint()
    word = request.json["word"].upper()
    game_id = request.json["gameId"]
    current_game = games[game_id]

    if not current_game.is_word_in_word_list(word):
        return jsonify(result = "not-word")
    elif not current_game.check_word_on_board(word):
        return jsonify(result = "not-on-board")
    else:
        current_game.play_and_score_word(word)
        return jsonify(result = "ok")





