#imports
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import sqlite3

#initialization and connection config. Config string should not change so long as UMood.db file is in same location as main
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UMood.db'

#Retreive all users
def get_all_users():
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM User")

    rows = cur.fetchall()
    con.close()
    users = [row_to_dict(row) for row in rows]
    return users

#insert user
def insert_user(user_Id, password, email, type):
    try:
        con = sqlite3.connect("UMood.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO User (User_ID, Password, Email, Type) VALUES (?, ?, ?, ?)",
                    (user_Id, password, email, type))
        con.commit()
        msg = "Record successfully added to database"
    except sqlite3.IntegrityError as e:
        con.rollback()
        msg = f"Error in the INSERT: {e}"
    finally:
        con.close()
        return msg

#retreive all emotions records
def get_all_emotions():
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Emotion")
    rows = cur.fetchall()
    con.close()
    emotions=[row_to_dict(row) for row in rows]
    return emotions

#insert emotion
def insert_emotion(emotion_Id, emotion, device, user_Id):
    try:
        con = sqlite3.connect("UMood.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO Emotion (Emotion_ID, Emotion, Device, User_ID) VALUES (?, ?, ?, ?)",
                    (emotion_Id, emotion, device, user_Id))
        con.commit()
        msg = "Record successfully added to database"
    except:
        con.rollback()
        msg = "Error in the INSERT"
    finally:
        con.close()
        return msg

#Converts a sqlite3.Row object to a dictionary for jsonify output
def row_to_dict(row):
    return dict(zip(row.keys(), row))

def get_emotions_in_interval(start_time, end_time):
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Adjust the SQL query to filter emotions within the specified time interval
    query = "SELECT * FROM Emotion WHERE Timestamp BETWEEN ? AND ?"
    cur.execute(query, (start_time, end_time))

    rows = cur.fetchall()
    con.close()
    
    emotions = [row_to_dict(row) for row in rows]
    return emotions

@app.route('/')
def hello():
    #function declared to data can change based on desired action ex select or insert get v insert
    data=get_all_emotions()
    return jsonify(data)

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        return jsonify(get_all_users())
    if request.method == 'POST':
        user_Id=request.form.get('user_Id')
        password=request.form.get('password')
        email=request.form.get('email')
        user_type=request.form.get('type')
        result_msg=insert_user(user_Id, password, email, user_type)
        return jsonify({"message": result_msg})

@app.route('/api/emotions', methods=['GET', 'POST'])
def handle_emotions():
    if request.method == 'GET':
        if 'start_time' in request.args:
            start_time = request.args.get('start_time')
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') 
            end_time = start_time + timedelta(minutes=30)           
            emotions = get_emotions_in_interval(start_time, end_time)
            return jsonify(emotions)  
        else: 
            return jsonify(get_all_emotions())
    elif request.method == 'POST':
        # Access form data
        emotion_Id = request.form.get('emotion_Id')
        emotion = request.form.get('emotion')
        device = request.form.get('device')
        user_Id = request.form.get('user_Id')
        # Call the insert_emotion function with form data
        result_msg = insert_emotion(emotion_Id, emotion, device, user_Id)
        return jsonify({"message": result_msg})
    
if __name__ == "__main__":
    app.run(debug=True)

#def 
# post: contrsuct query based off table args passed for json object ex emotion time then query database 


#def 
# get: within interval table info send 
    