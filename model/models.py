from .database import db #now we can create database table with the help of db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user_table"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(255))
    dob = db.Column(db.Date)
    user_type = db.Column(db.String(20), default="user")
    
    scores = db.relationship("Score", backref="user", cascade="all, delete") #User can have multiple score records

class Subject(db.Model):
    __tablename__ = "subject_table"
    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete") # A subject has multiple chapters
    

class Chapter(db.Model):
    __tablename__ = "chapter_table"
    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    subject_id = db.Column(db.Integer, db.ForeignKey("subject_table.subject_id"), nullable=False)
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete") # A chapter can have multiple quizzes


class Quiz(db.Model):
    __tablename__ = "quiz_table"
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter_table.chapter_id"), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=datetime.now, nullable=False)
    time_duration = db.Column(db.String(20), nullable=False) #hh:mm format
    remarks = db.Column(db.Text)

    questions = db.relationship("Question", backref="quiz", cascade="all, delete") # A quiz can have multiple questions
    scores = db.relationship("Score", backref="quiz", cascade="all, delete", lazy=True) # A quiz can have multiple scores.

    @property
    def question_count(self):
        return len(self.questions)


class Question(db.Model):
    __tablename__ = "question_table"
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_table.quiz_id"), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    question_title = db.Column(db.String(20), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

class Score(db.Model):
    __tablename__ = "score_table"
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_table.quiz_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.user_id"), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.now, nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)