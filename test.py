from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """initialize"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    
    def test_homepage(self):
        """test if all data display"""
        with self.client:
            response = self.client.get("/")
            self.assertIn("board", session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b' <p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
    def test_valid_word(self):
        """test valid word"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R","U", "B", "B"],
                                 ["R","U", "B", "B"],
                                 ["R","U", "B", "B"]]
        response = self.client.get('checking-word?word=rub')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """test invalid word"""
        self.client.get("/")
        response = self.client.get("/checking-word?word=lkqjl")
        self.assertEqual(response.json['result'], 'not-word')

    def test_valid_word_nob(self):
        """test valid word not on board"""
        self.client.get('/')
        response = self.client.get("/checking-word?word=click")
        self.assertEqual(response.json['result'], 'not-on-board')
