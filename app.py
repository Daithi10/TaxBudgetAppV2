from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# =======================
# Flask App Configuration
# =======================
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a strong secret key

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/yourdbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =======================
# Database Models
# =======================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    budgets = db.relationship('Budget', backref='user', lazy=True)

class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    budget_name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    marital = db.Column(db.String(20))
    children = db.Column(db.Integer)
    age_group = db.Column(db.String(20))
    tax_credits = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =======================
# Routes
# =======================

# Home page
@app.route("/")
def home():
    return render_template("base.html")

# Budget page
@app.route("/budget", methods=["GET", "POST"])
def budget():
    if request.method == "POST":
        username = request.form.get("username")
        budget_name = request.form.get("budget_name")
        salary = float(request.form.get("salary"))
        marital = request.form.get("marital")
        children = int(request.form.get("children", 0))
        age_group = request.form.get("age_group")
        tax_credits = float(request.form.get("tax_credits", 0))

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found. Please register.", "danger")
            return redirect(url_for("budget"))

        new_budget = Budget(
            user_id=user.id,
            budget_name=budget_name,
            salary=salary,
            marital=marital,
            children=children,
            age_group=age_group,
            tax_credits=tax_credits
        )
        db.session.add(new_budget)
        db.session.commit()
        flash("Budget saved successfully!", "success")
        return redirect(url_for("budget"))

    return render_template("budget.html")

# Tax page (can merge with budget if desired)
@app.route("/tax", methods=["GET", "POST"])
def tax():
    # Currently acts the same as budget for placeholder
    return render_template("tax.html")

# Contacts page
@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        contact_entry = Contact(name=name, email=email, message=message)
        db.session.add(contact_entry)
        db.session.commit()
        flash("Message sent successfully!", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_pw = generate_password_hash(password, method="sha256")

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("register"))

        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome {user.username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

# Forgot Password page placeholder
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return render_template("forgot_password.html")

# Reset Password page placeholder
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    return render_template("reset_password.html")

# Saved Budget page
@app.route("/saved-budget")
def saved_budget():
    if "user_id" in session:
        user_budgets = Budget.query.filter_by(user_id=session["user_id"]).all()
        return render_template("saved_budget.html", budgets=user_budgets)
    else:
        flash("Please log in to view saved budgets.", "danger")
        return redirect(url_for("login"))

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

# =======================
# Run the App
# =======================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
    app.run(debug=True)
