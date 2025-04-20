from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
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

# homepage route
@app.route("/", methods=["GET", "POST"])
def index():
    print("SESSION START:", dict(session))

     # Only choose a new word if it's not already in session
    if "word" not in session or "guessed" not in session or "wrong" not in session:
        words = Word.query.all()
        if not words:
            return "No words in database!"
        selected_word = random.choice(words).text
        session["word"] = selected_word
        session["guessed"] = []  # 🔥 Initialize guessed letter list
        session["wrong"] = 0 # initialize sessopm wrong if not set


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

    print("SESSION END:", dict(session))
    print("Selected Word:", session.get("word"))
    print("Guessed Letters:", session.get("guessed"))
    print("Wrong Guess Count:", session.get("wrong"))
    print("SECRET KEY USED:", app.secret_key)
    return render_template(
        "index.html", 
        word=selected_word, 
        blanks=blank_word, 
        guess=guessed_letter, 
        guessed=guessed_letters, 
        wrong=wrong,
        status=game_status
)

# reset route
@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

# run app / create database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
    app.run(debug=True, host="0.0.0.0")

