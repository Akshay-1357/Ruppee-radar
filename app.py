from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budjet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
categories = ['Food','Social Life', "Pets","Transport","Health","Education","Shopping","Bills & Fees","Gifts","Others"]
sources = ['Investments','Salary','Savings','Others']

# Models
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default= datetime.utcnow,nullable=False)


# Create tables
with app.app_context():
    db.create_all()

# Routes

@app.route('/dashboard')
def home():
    return render_template('dashboard.html')

# Expense page
@app.route('/expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        if category and amount:
            new_expense = Expense(name=category, amount=float(amount))
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('expense'))
    all_expenses = Expense.query.all()
    return render_template('expense.html', expenses=all_expenses, cats = categories)

# Income page
@app.route('/income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        source = request.form['source']
        amount = request.form['income']
        date = request.form['date']
        if source and amount:
            new_income = Income(source=source, amount=float(amount),date= datetime.strptime(date, '%Y-%m-%d'))
            db.session.add(new_income)
            db.session.commit()
            return redirect(url_for('add_income'))
    all_income =  Income.query.order_by(Income.date.desc()).all()
    return render_template('income.html', incomes=all_income , srcs = sources)



@app.route('/income_data', methods=['GET'])
def income_data():
    all_income = Income.query.order_by(Income.date.desc()).all()
    income_list = []
    for inc in all_income:
        income_list.append({
            'source': inc.source,
            'amount': inc.amount,
            'date': inc.date.strftime('%Y-%m-%d')  # Format date as string
        })
    return jsonify(income_list)


@app.route('/layout')
def test_layout():
    return render_template('test.html')

@app.route('/transactions')
def transactions():
    all_expenses = Expense.query.all()
    all_income = Income.query.all()
    return render_template('transactions.html', expenses=all_expenses, incomes=all_income)

@app.route('/graph')
def Graph():
    return render_template('graph.html')


if __name__ == '__main__':
    app.run(debug=True)

