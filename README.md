Tax & Budget App
Overview

The Tax & Budget App is a Flask web application designed to help users track their monthly income, expenses, and savings. Users can calculate residual income, decide on savings percentage, and save budget history when registered.

This project uses Flask, Flask-SQLAlchemy, and SQLite/PostgreSQL for the database.

Features

User registration and login with secure password hashing.

Monthly budget tracking: income, rent, groceries, transport, utilities, and other expenses.

Calculate residual income after expenses.

Determine savings amount based on a user-defined percentage.

Save budgets for registered users.

View previously saved budgets.

Contact form for feedback.

Tech Stack

Backend: Python, Flask

Database: SQLite or PostgreSQL

Frontend: HTML, CSS, Jinja2 Templates

Security: Werkzeug password hashing

Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/TaxBudgetAppV2.git
cd TaxBudgetAppV2


Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux


Install dependencies:

pip install -r requirements.txt


Initialize the database:

python
>>> from app import db, app
>>> with app.app_context():
...     db.create_all()


Run the application:

flask run


The app will be available at http://127.0.0.1:5000/.

Usage

Home Page: Login or register to access the budget tracker.

Budget Tracker: Enter income and expenses, then calculate residual income.

Savings: Specify the percentage of residual income to save and save the budget (requires login).

Saved Budgets: View previously saved budgets (requires login).

Database Schema

User Table

id

fullname

username

email

password

security_question

security_answer

Budget Table

id

budget_name

income

rent

groceries

transport

utilities

other

savings_percent

savings_amount

marital

children

age_group

tax_credits

user_id

created_at

Contact Table

id

name

email

message

created_at

Notes

Passwords are securely hashed using pbkdf2:sha256.

The app requires the user to exist before saving budgets due to foreign key constraints.

Make sure the database file (app.db) or instructions to recreate it are included for deployment.

Author

Mbata David Junior
