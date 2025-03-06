from flask import Blueprint
from flask import redirect, url_for, render_template, request, flash
from model.models import db, User
from sqlalchemy.exc import IntegrityError
from datetime import datetime

user = Blueprint("user", __name__, template_folder="templates", static_folder="static")


@user.route("/login/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        #handle the request
        email = request.form.get("email") #fetching the email from form
        password = request.form.get("password") #fetching the password from form

        reg_user = User.query.filter_by(email=email).first() #filtering the users by its Email

        if reg_user:
            if reg_user.password == password:
                if reg_user.user_type == "Admin":
                    return redirect(url_for("admin.admin_dashboard")) # if the user is admin
                else:
                    return redirect(url_for("user.user_dashboard")) # if any user wants to login
            else:
                flash("Email or Password is incorrect", "error") # for incorrect email or password
                return redirect(url_for("user.login"))
        else:
            flash("User does not exists", "error") # if an unregistered user wants to login
            return redirect(url_for("user.login"))
    else:
        return render_template("login.html") # if other than post request is applied
    

@user.route("/register/", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        #handle request
        try:
            dob = request.form["dob"]
            dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
            new_user = User(
                username = request.form["username"],
                email = request.form["email"],
                password = request.form["password"],
                full_name = request.form["full_name"],
                qualification = request.form["qualification"],
                dob = dob_obj,
            )
        except IntegrityError:
            db.session.rollback()
            flash("User has already exists", "error")
            
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("user.login"))


    return redirect(url_for("admin.admin_dashboard"))

@user.route("/user_dashboard/")
def user_dashboard():
    return "hello User!"