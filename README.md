To spin up backend 
1: run $ pip install -r requirements.txt
2: $ pip install -r requirements.txt
3: go to terminal (terminal should be open to UMood git project location)
4: $ sqlite 3 UMood.db
5: $ CREATE TABLE User (
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Create_Time DATETIME DEFAULT CURRENT_TIMESTAMP,
    Password VARCHAR(16) NOT NULL,
    Email VARCHAR(16) NOT NULL,
    Type INTEGER NOT NULL,
    UNIQUE (User_ID)
);
CREATE TABLE Emotion (
    Emotion_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Emotion VARCHAR(16) NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Device VARCHAR(16) NOT NULL,
    User_ID INTEGER NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES User (User_ID),
    UNIQUE (Emotion_ID)
); - Should be able to run all in one copy/paste
6: Make sure UMood.db, .venv, .env and wtv else applicable is in .gitignore

After that setup, you should be able to use functions in main to query the database; show table info and insert into tables