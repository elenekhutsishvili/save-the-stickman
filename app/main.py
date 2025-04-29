from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_secret")
# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'words.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# table structure 
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Word {self.text}>"

# User table structure
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Securely hashed version of the user's password
    password_hash = db.Column(db.String(128), nullable=False)
    games_played = db.Column(db.Integer, default=0)
    games_won = db.Column(db.Integer, default=0)

    # Hash the password before saving to database
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check if the given password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # String representation of the user (for debugging/logging)
    def __repr__(self):
        return f"<User {self.email}>"

# Route to handle login and registration
@app.route("/login", methods=["GET", "POST"])
def login():
    message = None  # Feedback message to show on the page

    if request.method == "POST":
        # Get email and password from the form
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        user = User.query.filter_by(email=email).first()

        if user:
            # If user exists, verify the password
            if user.check_password(password):
                session["user_id"] = user.id  # Save user ID in session
                message = "Logged in successfully!"
                return redirect("/")  # Go to the game page
            else:
                message = "Incorrect password."
        else:
            # If user does not exist, create a new account
            new_user = User(email=email)
            new_user.set_password(password)  # Securely hash the password
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id  # Log the user in
            message = "Account created successfully!"
            return redirect("/")  # Go to the game page

    # For GET requests, just show the login form
    return render_template("login.html", message=message)

def get_stickman_stage(wrong_guesses):
    stickman_stages = [
        "",  # 0 wrong
        "😵",  # 1 wrong
        "😵\n🪢",  # 2 wrong
        "😵\n🫲🪢",  # 3 wrong
        "😵\n🫲🪢🫱",  # 4 wrong
        "😵\n🫲🪢🫱\n🦵",  # 5 wrong
        "😵\n🫲🪢🫱\n🦵🦿"  # 6 wrong
    ]
    return stickman_stages[min(wrong_guesses, 6)]


# homepage route
@app.route("/", methods=["GET", "POST"])
def index():
    # 🔐 Redirect to login if not logged in
    if "user_id" not in session:
        return redirect("/login")


     # Only choose a new word if it's not already in session
    if "word" not in session or "guessed" not in session or "wrong" not in session:
        words = Word.query.all()
        if not words:
            return "No words in database!"
        selected = random.choice(words).text
        session["word"] = selected
        session["guessed"] = []  # 🔥 Initialize guessed letter list
        session["wrong"] = 0 # initialize sessopm wrong if not set
        session["hint_used"] = False  # 🔥 Initialize hint_used


    # Pull values from session
    selected_word = session["word"]
    guessed_letters = session["guessed"]
    wrong = session["wrong"]


    guessed_letter = None
    if request.method == "POST":
        guessed_letter = request.form.get("letter")

        if guessed_letter:
            guessed = session.get("guessed", [])

            if guessed_letter.lower() not in guessed:
                guessed.append(guessed_letter.lower())
                session["guessed"] = guessed

                if guessed_letter.lower() not in selected_word:
                    wrong += 1
                    session["wrong"] = wrong
           

    # 🔍 Build the displayed blank word with guessed letters revealed
   
    #show correct guesses hide others
    blank_word = " ".join([letter if letter in guessed_letters else "_" for letter in selected_word])

    # Determine game status
    game_status = "playing"

    if "_" not in blank_word:
        game_status = "win"
    elif wrong >= 6:
        game_status = "lose"


    # Only update stats if the game is over
    if game_status in ["win", "lose"] and "user_id" in session:
        user = User.query.get(session["user_id"])
        if user:
            user.games_played += 1
            if game_status == "win":
                user.games_won += 1
            db.session.commit()

    # Now get stats to display
    user_email = None
    games_played = None
    games_won = None

    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if user:
            user_email = user.email
            games_played = user.games_played
            games_won = user.games_won        


    stickman = get_stickman_stage(wrong)

    return render_template(
        "index.html", 
        word=selected_word,
        blanks=blank_word, 
        guess=guessed_letter, 
        guessed=guessed_letters, 
        wrong=wrong,
        status=game_status,
        user_email=user_email,
        games_played=games_played,
        games_won=games_won,
        stickman=stickman

)

# reset route
@app.route("/reset")
def reset():
    # Save the user's ID before clearing session
    user_id = session.get("user_id")

    # Clear everything else (word, guessed, wrong, etc.)
    session.clear()

    # Restore the user so they don't get logged out
    if user_id:
        session["user_id"] = user_id

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()  # Clear all session data
    return redirect("/login")  # Send user back to login page

@app.route("/hint")
def hint():
    if "word" in session and "guessed" in session:
        word = session["word"]
        guessed = session["guessed"]

        # 🛑 First check if game is still playing
        blanks = " ".join([letter if letter in guessed else "_" for letter in word])

        if "_" not in blanks or session.get("wrong", 0) >= 6:
            # Game already won or lost → do not give hints
            return redirect("/")

        # 🛑 Check if hint is already used
        if session.get("hint_used", False):
            # Hint already used, do nothing
            return redirect("/")


        # Find unguessed letters in the word
        unguessed_letters = [letter for letter in word if letter not in guessed]

        if unguessed_letters:
            # Pick one random unguessed letter
            new_hint_letter = random.choice(unguessed_letters)
            guessed.append(new_hint_letter)
            session["guessed"] = guessed
            session["hint_used"] = True  # 🔥 Mark hint as used!


    return redirect("/")

# run app / create database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
    app.run(debug=True, host="0.0.0.0")

