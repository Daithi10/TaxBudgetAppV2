import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =======================
# Database Models
# =======================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=True)  # optional
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    security_question = db.Column(db.String(200), nullable=False)
    security_answer = db.Column(db.String(200), nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_name = db.Column(db.String(100), nullable=True)
    income = db.Column(db.Float, nullable=False)
    rent = db.Column(db.Float, nullable=False)
    groceries = db.Column(db.Float, nullable=False)
    transport = db.Column(db.Float, nullable=False)
    utilities = db.Column(db.Float, nullable=False)
    other = db.Column(db.Float, nullable=False)
    savings_percent = db.Column(db.Float)
    savings_amount = db.Column(db.Float)
    marital = db.Column(db.String(20), nullable=True)
    children = db.Column(db.Integer, nullable=True)
    age_group = db.Column(db.String(20), nullable=True)
    tax_credits = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =======================
# Routes
# =======================

@app.route("/")
def home():
    return render_template("index.html")  # your landing page template


# -----------------------
# Registration
# -----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        security_question = request.form.get("security_question")
        security_answer = request.form.get("security_answer")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("register"))

        # ✅ Correct hashing method
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(
            fullname=fullname,
            username=username,
            email=email,
            password=hashed_pw,
            security_question=security_question,
            security_answer=security_answer
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------
# Login
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# -----------------------
# Logout
# -----------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("home"))

# -----------------------
# Budget Tracker
# -----------------------
@app.route("/budget", methods=["GET", "POST"])
def budget():
    if "user_id" not in session:
        flash("Please log in to save a budget.", "warning")
    
    residual_income = None
    savings_amount = None
    savings_percent = None

    if request.method == "POST":
        action = request.form.get("action")

        try:
            # Common fields for both calculate and save
            income = float(request.form.get("income"))
            rent = float(request.form.get("rent"))
            groceries = float(request.form.get("groceries"))
            transport = float(request.form.get("transport"))
            utilities = float(request.form.get("utilities"))
            other = float(request.form.get("other"))

            residual_income = income - (rent + groceries + transport + utilities + other)

            if action == "calculate":
                if request.form.get("savings"):
                    savings_percent = float(request.form.get("savings"))
                    savings_amount = residual_income * savings_percent / 100

            elif action == "save":
                if "user_id" not in session:
                    flash("You must be logged in to save a budget.", "danger")
                    return redirect(url_for("budget"))

                savings_percent = float(request.form.get("savings"))
                savings_amount = residual_income * savings_percent / 100

                new_budget = Budget(
                    budget_name=request.form.get("budget_name", "My Budget"),
                    income=income,
                    rent=rent,
                    groceries=groceries,
                    transport=transport,
                    utilities=utilities,
                    other=other,
                    savings_percent=savings_percent,
                    savings_amount=savings_amount,
                    user_id=session["user_id"]
                )
                db.session.add(new_budget)
                db.session.commit()
                flash("Budget saved successfully!", "success")
                return redirect(url_for("budget"))

        except Exception as e:
            flash(f"Error processing budget: {e}", "danger")
    
    return render_template(
        "budget.html",
        residual_income=residual_income,
        savings_amount=savings_amount,
        savings_percent=savings_percent
    )

# -----------------------
# Tax Calculator
# -----------------------
@app.route("/tax", methods=["GET", "POST"])
def tax():
    result = None
    breakdown = None
    salary = 0

    if request.method == "POST":
        income = float(request.form.get("income"))
        marital_status = request.form.get("marital_status")
        children_count = int(request.form.get("children_count", 0))
        age_group = request.form.get("age_group")
        employment_type = request.form.get("employment_type")
        tax_credits = float(request.form.get("tax_credits", 0))

        # Placeholder tax calculation logic
        tax_rate = 0.2  # example flat rate
        result = income * tax_rate - tax_credits
        breakdown = {"Income Tax": income * tax_rate, "Tax Credits": tax_credits}

    return render_template("tax.html", result=result, breakdown=breakdown, income=income)

# -----------------------
# Contact Form
# -----------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        flash("Message sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# -----------------------
# Saved Budgets
# -----------------------
@app.route("/saved_budgets")
def saved_budgets():
    if "user_id" not in session:
        flash("Please log in to view your saved budgets.", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    budgets = Budget.query.filter_by(user_id=user_id).order_by(Budget.created_at.desc()).all()

    return render_template("saved_budget.html", budgets=budgets)


# -----------------------
# Reset Password Placeholder
# -----------------------
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    # Implement actual reset logic later
    if request.method == "POST":
        flash("Password reset functionality not implemented yet.", "info")
        return redirect(url_for("login"))

    return render_template("reset_password.html", username=session.get("username"), question="Your security question here")

with app.app_context():
    db.drop_all()
    db.create_all()

# =======================
# Run App
# =======================
if __name__ == "__main__":
    # Create tables if not exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)

with app.app_context():
    db.create_all()


