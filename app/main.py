from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
# secret key
app.secret_key = "secret_key"
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
     # Only choose a new word if it's not already in session
    if "word" not in session:
        words = Word.query.all()
        if not words:
            return "No words in database!"
        selected_word = random.choice(words).text
        session["word"] = selected_word
        session["guessed"] = []  # 🔥 Initialize guessed letter list

    else:
        selected_word = session["word"]

    guessed_letter = None
    if request.method == "POST":
        guessed_letter = request.form.get("letter")

        if guessed_letter:
            guessed = session.get("guessed", [])
            if guessed_letter.lower() not in guessed:
                guessed.append(guessed_letter.lower())
                session["guessed"] = guessed
           

    # 🔍 Build the displayed blank word with guessed letters revealed
    #get guessed letter from session
    guessed_letters = session.get("guessed", [])
    #show correct guesses hide others
    blank_word = " ".join([letter if letter in guessed_letters else "_" for letter in selected_word])

    return render_template("index.html", word=selected_word, blanks=blank_word, guess=guessed_letter, guessed=guessed_letters)

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

