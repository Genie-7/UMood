#imports
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template, session, url_for, redirect
import sqlite3


#initialization and connection config. Config string should not change so long as UMood.db file is in same location as main
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

def get_user_by_id(user_id):
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    query="SELECT * FROM User WHERE User_ID = ?"
    cur.execute(query, (user_id))

    row = cur.fetchone()
    con.close()
    if row:
        user = row
        return user
    else:
        return None

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

#register user
def register_user(password, email, type):
    try:
        con = sqlite3.connect("UMood.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO User (Password, Email, Type) VALUES (?, ?, ?)",
                    (password, email, type))
        con.commit()
        msg = "User successfully registered"
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
def home():
    #function declared to data can change based on desired action ex select or insert get v insert
    return render_template('home.html')

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    #get all users info
    if request.method == 'GET':
        return jsonify(get_all_users())
    #input(register) user
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
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        print("H1"+email+password)
        result_msg=register_user(password, email, 2)
        print("H2"+result_msg)
        if result_msg=="User successfully registered":
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        password=request.form.get('password')
        email=request.form.get('email')
        user = authenticate_user(email, password)
        if user:
            # Successful login, perform any additional actions here
            session['user_id'] = user['User_ID']
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials, handle accordingly (e.g., show error message)
            print("Invalid Credentials")
            return render_template('login.html')
    return render_template('login.html')

def authenticate_user(email, password):
    con = sqlite3.connect("UMood.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # Retrieve user information based on the provided email
    cur.execute("SELECT * FROM User WHERE Email = ? AND Password = ?", (email, password))
    user = cur.fetchone()
    con.close()
    if user:
        return user
    else:
        return None

@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        return render_template('dashboard.html', user_id=user_id)
    else:
        return 'Not logged in'

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
        
if __name__ == "__main__":
    app.run(debug=True)

    