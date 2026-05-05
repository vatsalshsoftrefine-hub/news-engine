from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/")
def root():
    return render_template("login.html")

@ui_bp.route("/login")
def login():
    return render_template("login.html")

@ui_bp.route("/register")
def register():
    return render_template("register.html")

@ui_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@ui_bp.route("/interests")
def interests():
    return render_template("interests.html")

@ui_bp.route("/analytics")
def analytics_page():
    return render_template("analytics.html")