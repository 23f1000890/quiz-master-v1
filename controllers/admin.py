from flask import Blueprint

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/admin_dashboard")
def admin_dashboard():
    return "hello admin"