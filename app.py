from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budjet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)


# Create tables
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def home():
    return redirect(url_for('add_expense'))

# Expense page
@app.route('/expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        if name and amount:
            new_expense = Expense(name=name, amount=float(amount))
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('add_expense'))
    all_expenses = Expense.query.all()
    return render_template('expense.html', expenses=all_expenses)

# Income page
@app.route('/income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        source = request.form['source']
        amount = request.form['amount']
        if source and amount:
            new_income = Income(source=source, amount=float(amount))
            db.session.add(new_income)
            db.session.commit()
            return redirect(url_for('add_income'))
    all_income = Income.query.all()
    return render_template('income.html', incomes=all_income)

@app.route('/layout')
def test_layout():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)

