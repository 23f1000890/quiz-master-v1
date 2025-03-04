# first import flask to start a flask project
from flask import Flask
from model.models import db, User
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv() #load variables from .env file



app = Flask(__name__) #create app

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) #database initialization
with app.app_context():  
    db.create_all()
    admin = User.query.filter_by(username="admin123").first()
    if not admin:
        admin = User(username="admin123", password="1234", full_name="Chirantan Chakraborty", user_type="Admin")
        db.session.add(admin)
        db.session.commit()



@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True) #run app