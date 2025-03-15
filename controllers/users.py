from flask import Blueprint
from flask import redirect, url_for, render_template, request, flash
from model.models import * # import all from models.py
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app_user = Blueprint("app_user", __name__, template_folder="templates", static_folder="static")


@app_user.route("/login/", methods = ["GET", "POST"])
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
                    return redirect(url_for("app_user.user_dashboard", user_id=reg_user.user_id)) # if any user wants to login
            else:
                flash("Email or Password is incorrect", "error") # for incorrect email or password
                return redirect(url_for("app_user.login"))
        else:
            flash("User does not exists", "error") # if an unregistered user wants to login
            return redirect(url_for("app_user.login"))
    else:
        return render_template("login.html") # if other than post request is applied
    

@app_user.route("/register/", methods = ["GET", "POST"])
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

        return redirect(url_for("app_user.login"))


    return redirect(url_for("admin.admin_dashboard"))

# user dashboard of home screen
@app_user.route("/user_dashboard/<int:user_id>")
def user_dashboard(user_id):
    reg_user = User.query.filter_by(user_id=user_id).first_or_404()
    quizzes = Quiz.query.all()

    return render_template("user_dashboard.html", reg_user=reg_user, quizzes=quizzes)


# the quiz interface
@app_user.route("/user_dashboard/<int:user_id>/quiz/<int:quiz_id>", methods=["GET", "POST"])
def quiz(user_id,quiz_id):
    reg_user = User.query.get_or_404(user_id)
    quiz = Quiz.query.get_or_404(quiz_id)  # Fetch the quiz
    questions = quiz.questions # Fetch the specific question by its ID
    total = len(questions)

    if request.method == "POST":
        # Handle quiz submission
        total_score = 0
        for question in questions:
            selected_answer = request.form.get(f"question_{question.question_id}")
            if selected_answer == question.correct_answer:
                total_score += 1
        
        new_score = Score(user_id=user_id, quiz_id=quiz_id, total_scored=total_score)
        db.session.add(new_score)
        db.session.commit()

        return redirect(url_for("app_user.submit_quiz", user_id=user_id))

    return render_template("quiz.html", reg_user=reg_user, questions=questions, quiz=quiz, total=total)


@app_user.route("/user_dashboard/<int:user_id>/scoreboard")
def submit_quiz(user_id):
    reg_user = User.query.filter_by(user_id=user_id).first_or_404()
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.desc()).all()
    
    return render_template(
        "submit_quiz.html",
        reg_user=reg_user,
        scores=scores
    )


#View the Quiz details
@app_user.route("/user_dashboard/<int:user_id>/view_quiz/<int:quiz_id>")
def view_quiz(user_id,quiz_id):
    quiz = Quiz.query.get(quiz_id) # fetch specific quiz by id
    reg_user = User.query.filter_by(user_id=user_id).first_or_404()

    return render_template("view_quiz.html", quiz=quiz, reg_user=reg_user)

