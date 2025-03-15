from flask import Blueprint
from flask import render_template, redirect, url_for, request
from model.models import * # to fetch all tables from .models
from sqlalchemy.exc import IntegrityError

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/user_details/")
def user_details():
    users = User.query.filter_by(user_type="user").all()
    reg_admin = User.query.filter_by(user_type="Admin").first_or_404()
    return render_template("user_details.html", users=users, reg_admin=reg_admin)

@admin.route("/admin_dashboard/")
def admin_dashboard():
    reg_admin = User.query.filter_by(user_type="Admin").first_or_404()
    query = request.args.get("search", "").strip() # Get the search query from URL
    if query:
        subjects = Subject.query.filter(Subject.subject_name.ilike(f"%{query}%")).all()
    else:
        subjects = Subject.query.all()
    
    return render_template("admin_dashboard.html", reg_admin=reg_admin, subjects=subjects, query=query)


# Subject Management - Create, Add, Update, Delete
@admin.route("/add_subject/", methods = ["GET", "POST"])
def add_subject():
    # if request.method == "GET":
    #     return render_template("add_subjects.html")
    if request.method == "POST":
        #handle the request
        try:
            new_subject = Subject(
                subject_name = request.form["subject_name"], #fetching name from subject form
                description = request.form["description"],  #fetching description from subject form
            )
        except IntegrityError:
            db.session.rollback()
        
        db.session.add(new_subject)
        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))

    return render_template("add_subjects.html")

@admin.route("/edit_subject/<int:subject_id>", methods = ["GET", "POST"])
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id) # fetch subject by id

    if request.method == "POST":
        if subject:
            subject.subject_name = request.form.get("subject_name") #update name
            subject.description = request.form.get("description") #update description
            db.session.commit()
            return redirect(url_for("admin.admin_dashboard"))
        return redirect(url_for("admin.add_subject"))

    return render_template("edit_subjects.html", subject=subject)

@admin.route("/delete_subject/<int:subject_id>")
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id) # fetch subject by id
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for("admin.admin_dashboard"))
    return "Subject not found", 404


#Chapter management - Create, Read, Update, Delete
@admin.route("/add_chapter/<int:subject_id>", methods = ["GET", "POST"])
def add_chapter(subject_id):
    subject = Subject.query.get(subject_id) # fetch subject id from subject table to connect with chapter

    if request.method == "POST":
        #handle the request
        try:
            new_chapter = Chapter(
                chapter_name = request.form["chapter_name"], #fetching name from chapter form
                description = request.form["description"],  #fetching description from chapter form
                subject_id = subject.subject_id
            )
        except IntegrityError:
            db.session.rollback()
        
        db.session.add(new_chapter)
        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))

    return render_template("add_chapters.html", subject=subject, subject_id=subject_id)

@admin.route("/edit_chapter/<int:chapter_id>", methods = ["GET", "POST"])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id) # fetch subject by id

    if request.method == "POST":
        if chapter:
            chapter.chapter_name = request.form.get("chapter_name") #update name
            chapter.description = request.form.get("description") #update description
            db.session.commit()
            return redirect(url_for("admin.admin_dashboard"))
        return redirect(url_for("admin.add_chapter"))

    return render_template("edit_chapters.html", chapter=chapter)

@admin.route("/delete_chapter/<int:chapter_id>")
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id) # fetch subject by id
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        return redirect(url_for("admin.admin_dashboard"))
    return "Chapter not found", 404


#Quiz Management
@admin.route("/quiz_dashboard/")
def quiz_dashboard():
    reg_admin = User.query.filter_by(user_type="Admin").first_or_404()
    quizzes = Quiz.query.all()
    
    return render_template("quiz_dashboard.html", reg_admin=reg_admin, quizzes=quizzes)


@admin.route("/add_quiz/", methods = ["GET", "POST"])
def add_quiz():
    chapters = Chapter.query.all()

    if request.method == "POST":
        #handle the request
        try:
            new_quiz = Quiz(
                chapter_id = request.form["chapter_id"],
                date_of_quiz = datetime.strptime(request.form["date_of_quiz"], "%Y-%m-%d"),
                time_duration = request.form["time_duration"],
                remarks = request.form["remarks"],
            )

        except IntegrityError:
            db.session.rollback()

        db.session.add(new_quiz)
        db.session.commit()

        return redirect(url_for("admin.quiz_dashboard"))


    return render_template("add_quiz.html", chapters=chapters)

@admin.route("/edit_quiz/<int:quiz_id>", methods = ["GET", "POST"])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id) # fetch quiz by id
    chapters = Chapter.query.all()

    if request.method == "POST":
        if quiz:
            quiz.chapter_id = request.form.get("chapter_id") #update chapter
            quiz.time_duration = request.form.get("time_duration") #update time of quiz
            quiz.date_of_quiz = datetime.strptime(request.form.get("date_of_quiz"), "%Y-%m-%d")  #update date of quiz
            quiz.remarks = request.form.get("remarks")
            db.session.commit()
            return redirect(url_for("admin.quiz_dashboard"))
        return redirect(url_for("admin.add_quiz"))

    return render_template("edit_quiz.html", quiz=quiz, chapters=chapters)

@admin.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for("admin.quiz_dashboard"))
    return "Quiz doesn't exist", 404

#question management - Create, Read, Update, Delete
@admin.route("/add_question/<int:quiz_id>", methods = ["GET", "POST"])
def add_question(quiz_id):
    quiz = Quiz.query.get(quiz_id) # fetch quiz id from quiz table to connect with question

    if request.method == "POST":
        #handle the request
        try:
            new_question = Question(
                question_statement = request.form["question_statement"],
                question_title = request.form["question_title"],
                option1 = request.form["option1"],
                option2 = request.form["option2"],
                option3 = request.form["option3"],
                option4 = request.form["option4"],
                correct_answer = request.form["correct_answer"],
                quiz_id = quiz.quiz_id,
            )
        except IntegrityError:
            db.session.rollback()
        
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for("admin.quiz_dashboard"))
    
    return render_template("add_question.html", quiz=quiz, quiz_id=quiz_id)

@admin.route("/edit_question/<int:question_id>", methods = ["GET", "POST"])
def edit_question(question_id):
    question = Question.query.get(question_id) # fetch question by id

    if request.method == "POST":
        if question:
            question.question_statement = request.form.get("question_statement")
            question.question_title = request.form.get("question_title")
            question.option1 = request.form.get("option1")
            question.option2 = request.form.get("option2")
            question.option3 = request.form.get("option3")
            question.option4 = request.form.get("option4")
            question.correct_answer = request.form.get("correct_answer")
            db.session.commit()
            return redirect(url_for("admin.quiz_dashboard"))
        return redirect(url_for("admin.add_question"))

    return render_template("edit_question.html", question=question)

@admin.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    question = Question.query.get(question_id) 
    if question:
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for("admin.quiz_dashboard"))
    return "Question not found", 404

@admin.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("admin.user_details"))
    return "ERROR", 404