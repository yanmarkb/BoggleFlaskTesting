
# Import the TestCase class from the unittest module, the app object from the app module, the session object from the Flask module, and the Boggle class from the boggle module.
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Define a new class called FlaskTests that inherits from the TestCase class.


class FlaskTests(TestCase):

    # This method is called before each test case is run. It sets up the test client and sets the app to testing mode.
    def setUp(self):
        """Stuff to do before every test."""

        # Create a new test client for the app.
        self.client = app.test_client()
        # Set the app to testing mode.
        app.config['TESTING'] = True

    # This test case tests that the homepage of the application is displayed correctly and that the necessary information is stored in the session.
    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        # Use the test client to make a GET request to the root URL of the app.
        with self.client:
            response = self.client.get('/')
            # Check that the 'board' key is in the session.
            self.assertIn('board', session)
            # Check that the 'highscore' key in the session is None.
            self.assertIsNone(session.get('highscore'))
            # Check that the 'nplays' key in the session is None.
            self.assertIsNone(session.get('nplays'))
            # Check that the string '<p>High Score:' is in the response data.
            self.assertIn(b'<p>High Score:', response.data)
            # Check that the string 'Score:' is in the response data.
            self.assertIn(b'Score:', response.data)
            # Check that the string 'Seconds Left:' is in the response data.
            self.assertIn(b'Seconds Left:', response.data)

    # This test case tests that the application can correctly identify a valid word on the Boggle board.
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        # Use the test client to make a GET request to the '/check-word' URL of the app, passing the word 'cat' as a query parameter.
        with self.client as client:
            with client.session_transaction() as sess:
                # Modify the 'board' key in the session to contain a specific set of letters.
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        # Check that the response JSON contains the string 'ok'.
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    # This test case tests that the application can correctly identify an invalid word on the Boggle board.
    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        # Use the test client to make a GET request to the root URL of the app.
        self.client.get('/')
        # Use the test client to make a GET request to the '/check-word' URL of the app, passing the word 'impossible' as a query parameter.
        response = self.client.get('/check-word?word=impossible')
        # Check that the response JSON contains the string 'not-on-board'.
        self.assertEqual(response.json['result'], 'not-on-board')

    # This test case tests that the application can correctly identify a non-English word on the Boggle board.
    def non_english_word(self):
        """Test if word is on the board"""

        # Use the test client to make a GET request to the root URL of the app.
        self.client.get('/')
        # Use the test client to make a GET request to the '/check-word' URL of the app, passing a random string of letters as a query parameter.
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        # Check that the response JSON contains the string 'not-word'.
        self.assertEqual(response.json['result'], 'not-word')
