"""
CREATE TABLE `User` (
  `User_ID` int(8) NOT NULL AUTO_INCREMENT,
  `Create_Time` datetime(6) NOT NULL DEFAULT current_timestamp(6),
  `Password` varchar(16) NOT NULL,
  `Email` varchar(16) NOT NULL,
  `Type` int(8) NOT NULL COMMENT 'either 1 (admin) or 2 (user)',
  PRIMARY KEY (`User_ID`),
  KEY `User_ID` (`User_ID`)
)

CREATE TABLE `Emotion` (
  `Emotion_ID` int(8) NOT NULL AUTO_INCREMENT,
  `Emotion` varchar(16) NOT NULL,
  `Timestamp` datetime(6) NOT NULL DEFAULT current_timestamp(6),
  `Device` varchar(16) NOT NULL,
  `User_ID` int(8) NOT NULL,
  PRIMARY KEY (`Emotion_ID`),
  KEY `emotion_fk` (`User_ID`),
  CONSTRAINT `emotion_fk` FOREIGN KEY (`User_ID`) REFERENCES `User` (`User_ID`)
)
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    User_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Create_Time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    Password = db.Column(db.String(16), nullable=False)
    Email = db.Column(db.String(16), nullable=False)
    Type = db.Column(db.Integer, nullable=False)