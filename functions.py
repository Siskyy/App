from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Function which checks whether the username and password match an entry within the database
def check_credentials(username, password):

    # First check the username
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        user_pass = cur.execute(f"SELECT password FROM User_data WHERE user_name = '{username}'").fetchone()[0]
        print(user_pass)

        # Now check if password matches
        if user_pass == password:
            print("You're in!")

            session["user_id"] = cur.execute(f"SELECT id FROM User_data WHERE user_name = '{username}'").fetchone()[0]
            session["username"] = cur.execute(f"SELECT user_name FROM User_data WHERE user_name = '{username}'").fetchone()[0]
            
            return redirect("/")
        else:
            print("WRONG!")
    return

def search_film(film):
    print(film)
    with sqlite3.connect("films.db") as con:
        cur = con.cursor()
        results = cur.execute(f"select title, year from movies where title LIKE '%{film}%' COLLATE NOCASE").fetchall()
    print(results)

    return results