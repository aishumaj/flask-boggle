from unittest import TestCase
from urllib.request import DataHandler

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            data = response.get_json()
            game_id = data["gameId"]
            board = data["board"]

            self.assertIsInstance(game_id, str)
            self.assertIsInstance(board, list)
            self.assertIsInstance(board[0], list)
            self.assertIn(game_id, games)

    def test_api_score_word(self):
        """Test scoring word on game board"""

        with self.client as client:

            game_id = client.post('/api/new-game').get_json()["gameId"]
            game = games[game_id]

            game.board = [
	    	["R","R","W","S","E"],
            ["L","T","Y","O","Y"],
	    	["A","V","B","S","R"],
		    ["P","O","N","R","I"],
		    ["L","N","T","E","O"]
             ]


           #test lap - result: ok
            resp = client.post(
                '/api/score-word',
                json = {"word": "LAP", "gameId": game_id}
            )
            data = resp.get_json()
            self.assertEqual({"result": "ok"}, data)

           #test dog - result: not-on-board
            resp = client.post(
                '/api/score-word',
                json = {"word": "DOG", "gameId": game_id}
            )
            data = resp.get_json()
            self.assertEqual({"result": "not-on-board"}, data)

           #test swe - result: not-word
            resp = client.post(
                '/api/score-word',
                json = {"word": "SWE", "gameId": game_id}
            )
            data = resp.get_json()
            self.assertEqual({"result": "not-word"}, data)


