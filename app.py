from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/expense_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Home page → Dashboard
@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total = sum(exp.amount for exp in expenses)
    return render_template("index.html", expenses=expenses, total=total, now=datetime.now())

# Add expense
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        category = request.form["category"]

        expense = Expense(description=description, amount=amount, category=category)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_expense.html", now=datetime.now())

# View all expenses
@app.route("/view")
def view_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total = sum(exp.amount for exp in expenses)
    return render_template("view_expenses.html", expenses=expenses, total=total, now=datetime.now())

# Delete expense
@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("view_expenses"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
