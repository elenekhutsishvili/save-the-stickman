from main import db, Word, app

with app.app_context():
    # Optional: clear old entries
    db.session.query(Word).delete()

    # Load words from words.txt
    with open("app/words.txt") as f:
        word_list = [line.strip() for line in f if len(line.strip()) >= 5]

    for w in word_list:
        db.session.add(Word(text=w))

    db.session.commit()

    print(f"{len(word_list)} words added successfully!")