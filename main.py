from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UMood.db'

def get_all_users():
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM User")

    rows = cur.fetchall()
    con.close()
    users = [row_to_dict(row) for row in rows]
    return users

def insert_user():
    try:
        con = sqlite3.connect("UMood.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO User (User_ID, Password, Email, Type) VALUES (3, 'Pass12', 'Alice@gmail.com', 1)")
        con.commit()
        con.close()
        msg = "Record successfully added to database"
    except:
        con.rollback()
        msg = "Error in the INSERT"
    finally:
        con.close()
        return msg

def get_all_emotions():
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Emotion")
    rows = cur.fetchall()
    con.close()
    emotions=[row_to_dict(row) for row in rows]
    return emotions

def insert_emotion():
    try:
        con = sqlite3.connect("UMood.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO Emotion (Emotion_ID, Emotion, Device, User_ID) VALUES (1, 'Happy', 'Mac', 1)")
        con.commit()
        con.close()
        msg = "Record successfully added to database"
    except:
        con.rollback()
        msg = "Error in the INSERT"
    finally:
        con.close()
        return msg

def row_to_dict(row):
    """Converts a sqlite3.Row object to a dictionary."""
    return dict(zip(row.keys(), row))

@app.route('/')
def hello():
    data=get_all_emotions()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
    