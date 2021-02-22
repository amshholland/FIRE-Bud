import sys
from datetime import datetime
from tempfile import mkdtemp
import mariadb

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
    ## response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure mysql to use SQLite database
try:
    conn = mariadb.connect(
        user='root', password='', host='localhost', port=3306, database='budget')
    cursor = conn.cursor()
except mariadb.Error as e:
    print("Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


@ app.route("/")
@ login_required
def index():
    """Show overview of budget"""

    return render_template("index.html")


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
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

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
            "SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("username must be unique", 403)
        else:
            # Hash password
            hash = generate_password_hash(password)

            insert = cursor.execute("""INSERT INTO users (username, hash) 
                                    VALUES (?, ?)""", (username, hash))
            conn.commit()

        # Direct user to login page
        return render_template("login.html")
        # return render_template("login.html")

    else:
        return render_template("register.html")


@ app.route("/project/templates/customize.php")
@ login_required
def customize():
    """Customize budget"""
    id = session["user_id"]
    # Direct user to customize.html page
    return render_template("customize.php", id=id)


@ app.route("/customized", methods=["POST"])
@ app.route("/project/templates/customized.php", methods=["GET", "POST"])
def customized():
    """Customize budget"""
    return ("ok")


@ app.route("/add", methods=["GET", "POST"])
@ login_required
def add():
    """Add to budget"""

    return render_template("register.html")


@ app.route("/budget", methods=["GET", "POST"])
@ login_required
def budget():
    """Complete monthly budget"""

    return render_template("register.html")


@ app.route("/net worth", methods=["GET", "POST"])
@ login_required
def net_worth():
    """Displays timeline of net worth"""

    return render_template("register.html")


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
