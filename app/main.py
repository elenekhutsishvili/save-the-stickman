from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
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

@app.route("/", methods=["GET", "POST"])
def index():
    words = Word.query.all()
    if not words:
        return "No words in database!"

    selected_word = random.choice(words).text
    blank_word = " ".join(["_" for _ in selected_word])
    guessed_letter = None
    if request.method == "POST":
        guessed_letter = request.form.get("letter")
        print(f"User guessed: {guessed_letter}")  # For now, just print it
    return render_template("index.html", word=selected_word, blanks=blank_word)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# run app / create database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
    app.run(debug=True, host="0.0.0.0")
