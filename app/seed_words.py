from main import db, Word, app

with app.app_context():
    # clear old entries
    db.session.query(Word).delete()

    # Load words from words.txt
    with open("app/words.txt") as f:
        # check length more than 5
        word_list = [line.strip() for line in f if len(line.strip()) >= 5]
    # add each word
    for w in word_list:
        db.session.add(Word(text=w))

    # save words
    db.session.commit()
    
    # print to check how many words were added
    print(f"{len(word_list)} words added successfully!")