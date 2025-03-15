# first import flask to start a flask project
from flask import Flask
from flask import redirect, url_for
from model.models import db, User
from controllers.users import app_user
from controllers.admin import admin
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv() #load variables from .env file



app = Flask(__name__) #create app

#flask configurations and modifications for the app
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#database initialization
db.init_app(app)
with app.app_context():  
    db.create_all()
    Admin = User.query.filter_by(username="admin123").first()
    if not Admin:
        Admin = User(username="admin123", email="admin@admin.com", password="1234", full_name="Chirantan Chakraborty", user_type="Admin")
        db.session.add(Admin)
        db.session.commit()

#registering blueprints to connect app to controllers
app.register_blueprint(app_user) # User route
app.register_blueprint(admin) # Admin route

@app.route("/")
def app_server():
    return redirect(url_for("app_user.login"))

#run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True) 