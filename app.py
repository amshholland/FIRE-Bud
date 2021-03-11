import gviz_api
import json
import datetime
from decimal import Decimal
from tempfile import mkdtemp
import mysql.connector
import pandas as pd
from dateutil.relativedelta import relativedelta


from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session)
from flask_session import Session
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure mysql to use SQLite database
try:
    conn = mysql.connector.connect(
        user='root', password='', host='localhost', port=3306, database='budget')
    cursor = conn.cursor()
except mysql.connector.Error as e:
    print("Error connecting to SQL Platform: {e}")
    sys.exit(1)


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in & their budget day
        session["user_id"] = rows[0][0]
        bud_day = rows[0][3]

        if not bud_day:
            return render_template("customize.html", bud_day=0)

        else:
            today = datetime.date.today()

            bud_day = datetime.date(today.year, today.month, bud_day)
            bud_month = bud_day + relativedelta(days=+1)

            if today < bud_day:
                bud_month = bud_month - relativedelta(months=1)

            session["bud_day"] = bud_day
            session["bud_month"] = bud_month
            print(bud_day)
            print(bud_month)

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@ app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@ app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Require that a user input a username
        if not username:
            return apology("must provide username", 403)

        # Require user to input a password
        elif not password:
            return apology("must provide password", 403)

        # Require user confirm password & ensure passwords match
        elif not password or not confirmation or confirmation != password:
            return apology("passwords must match", 403)

        # Check to see if username already exists
        cursor.execute(
            "SELECT * FROM users WHERE username = %s", (username,))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("username must be unique", 403)
        else:
            # Hash password
            hash = generate_password_hash(password)

            cursor.execute("""INSERT INTO users (username, hash)
                                    VALUES (%s, %s)""", (username, hash))
            conn.commit()

        # Direct user to customize page
        return render_template("customize.html")
        # return render_template("login.html")

    else:
        return render_template("register.html")


@app.route('/')
@ login_required
def index():
    """ Display MTD Budget Data"""
    id = session["user_id"]
    bud_month = session["bud_month"]

# AND bud_month = %s

    cursor.execute("""select category,
    sum(case when ie = 'expenseBud' then amount end) as bud,
    sum(case when ie = 'expense' then amount end) as actual
    from budget WHERE id = %s AND ie = %s OR ie = %s
    group by category""", (id, 'expenseBud', 'expense'))
    spend = cursor.fetchall()

    select = "SELECT category, SUM(amount) FROM budget WHERE id = %s AND ie = %s GROUP BY category"

    cursor.execute(select, (id, 'expenseBud'))
    expenses = cursor.fetchall()

    cursor.execute("""SELECT SUM(amount) FROM budget
    WHERE id = %s AND ie = %s OR ie = %s""", (id, 'billBud', 'expenseBud'))
    totalEx = float(cursor.fetchone()[0])

    cursor.execute(
        "SELECT SUM(amount) FROM budget WHERE id = %s AND ie = %s", (id, 'incomeBud'))
    income = float(cursor.fetchone()[0])

    remaining = income - totalEx

    return render_template("index.html", expenses=expenses, spend=spend, income=usd(income), totalEx=usd(totalEx), remaining=usd(remaining))


@ app.route("/add", methods=["POST"])
@ login_required
def add():

    if request.method == "POST":

        id = session["user_id"]
        bud_month = session["bud_month"]

        for ie, category, amount, date in zip(request.form.getlist('ie'),
                                              request.form.getlist(
                'category'),
                request.form.getlist(
                'amount'),
                request.form.getlist(
                'date')):
            if category and amount and date:
                cursor.execute("""INSERT INTO budget (id, ie, category, amount, date, bud_month)
                    VALUES (%s,%s,%s,%s,%s,%s)""", (id, ie, category, amount, date, bud_month))
                conn.commit()

    return render_template("index.html")


@ app.route("/customize")
@ login_required
def customize():
    """Customize budget"""
    id = session["user_id"]
    bud_day = session["bud_day"]
    print(bud_day)
    bud_month = session["bud_month"]

    select = "SELECT category FROM budget WHERE (id = %s) AND (ie = %s) GROUP BY category"

    cursor.execute(select, (id, "expenseBud"))
    expenses = cursor.fetchall()

    cursor.execute(select, (id, "incomeBud"))
    income = cursor.fetchall()

    cursor.execute(select, (id, "billBud"))
    bills = cursor.fetchall()

    return render_template("customize.html", bud_day=bud_day, expenses=expenses, income=income, bills=bills)


@ app.route("/transactions")
@ login_required
def transactions():
    """Add transactions"""

    id = session["user_id"]
    bud_day = session["bud_day"]

    select = "SELECT category FROM budget WHERE (id = %s) AND (ie = %s) GROUP BY category"
    cursor.execute(select, (id, "expenseBud"))
    expenses = cursor.fetchall()

    cursor.execute(select, (id, "incomeBud"))
    incomes = cursor.fetchall()

    cursor.execute(select, (id, "billBud"))
    bills = cursor.fetchall()

    return render_template("transactions.html", bud_day=bud_day, expenses=expenses, incomes=incomes, bills=bills)


@ app.route("/net_worth", methods=["GET", "POST"])
@ login_required
def net_worth():
    """Displays timeline of net worth"""
    id = session["user_id"]
    bud_month = session["bud_month"]

    if request.method == 'POST':
        for dsi, name, amount, rate in zip(request.form.getlist('dsi'),
                                           request.form.getlist('name'),
                                           request.form.getlist(
                'amount'),
                request.form.getlist('rate')):
            if dsi and name and amount:
                cursor.execute(
                    """INSERT INTO dsi (id, dsi, name, amount, rate, month)
                    VALUES (%s,%s,%s,%s,%s,%s)""", (id, dsi, name, amount, rate, bud_month))
                conn.commit()
        return render_template("net_worth.html")
    else:
        cursor.execute("""SELECT SUM(amount) FROM budget
        WHERE id = %s AND ie = %s OR ie = %s""", (id, 'bill', 'expense'))
        totalEx = float(cursor.fetchone()[0])

        cursor.execute(
            "SELECT SUM(amount) FROM budget WHERE id = %s AND ie = %s", (id, 'income'))
        income = float(cursor.fetchone()[0])

        remaining = income - totalEx
        print(remaining)

        select = "SELECT name, amount, rate FROM dsi WHERE (id = %s) AND (dsi = %s) GROUP BY name"
        cursor.execute(select, (id, "debt"))
        debts = cursor.fetchall()

        cursor.execute(select, (id, "savings"))
        savings = cursor.fetchall()

        cursor.execute(select, (id, "investment"))
        investments = cursor.fetchall()

        cursor.execute("""select month,
        sum(case when dsi='debt' then amount end) as debt,
        sum(case when dsi='savings' then amount end) as sav,
        sum(case when dsi='investment' then amount end) as inv
        from dsi WHERE id=%s
        group by month""", (id,))
        data = cursor.fetchall()

        return render_template("net_worth.html", debts=debts, savings=savings, investments=investments, data=data)


@ app.route("/goals", methods=["GET", "POST"])
@ login_required
def goals():
    """Determine monthly, yearly, and ultimate financial goals"""

    return render_template("goals.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    # Run the app server on localhost: 5000
    app.run('localhost', 5000)
