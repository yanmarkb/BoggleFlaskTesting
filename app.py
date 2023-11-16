from flask import Flask, jsonify, request, render_template, session
from boggle import Boggle

app = Flask(__name__)  # Create a Flask web application instance
app.config['SECRET_KEY'] = 'secretkey'  # Set a secret key for the application

boggle_game = Boggle()  # Create an instance of the Boggle game


@app.route('/')  # Define a route for the homepage
def home():
    """Render homepage."""
    board = boggle_game.make_board()  # Generate a new Boggle board
    session['board'] = board  # Store the board in the user's session
    # Get the user's high score from their session, or 0 if it doesn't exist
    highscore = session.get('highscore', 0)
    # Get the number of plays from the user's session, or 0 if it doesn't exist
    nplays = session.get('nplays', 0)

    # Render the homepage template with the board, high score, and number of plays
    return render_template('index.html', board=board, highscore=highscore, nplays=nplays)


@app.route('/check-word')  # Define a route for checking if a word is valid
def check_word():
    """Check if word is in dictionary."""
    word = request.args["word"]  # Get the word to check from the request arguments
    board = session["board"]  # Get the Boggle board from the user's session
    # Check if the word is valid on the board
    response = boggle_game.check_valid_word(board, word)

    # Return a JSON response with the result of the word check
    return jsonify({'result': response})


# Define a route for posting a score
@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json['score']  # Get the score from the request JSON
    # Get the user's high score from their session, or 0 if it doesn't exist
    highscore = session.get('highscore', 0)
    # Get the number of plays from the user's session, or 0 if it doesn't exist
    nplays = session.get('nplays', 0)

    # Increment the number of plays in the user's session
    session['nplays'] = nplays + 1
    # Update the user's high score if the new score is higher
    session['highscore'] = max(score, highscore)

    # Return a JSON response indicating whether the user broke their high score
    return jsonify(brokeRecord=score > highscore)
