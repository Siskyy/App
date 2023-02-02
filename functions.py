from flask import redirect, session, flash
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
    # First check the username in the database
    with sqlite3.connect("database.db") as con: # connects to the database
        cur = con.cursor()
        # Checks wether there is a password for the username inputted by the user
        # If the user enters a username that does not exist, a password will not be found
        user_pass = cur.execute(f"SELECT password FROM users WHERE username = '{username}'").fetchone()
        if user_pass == None:
            message = f"User '{username}' does not exist!"
            return [False, message]
        else:
            user_pass = user_pass[0]

        # Now check if password matches
        if user_pass == password:
            # If the password is correct the session data is set to the user who just logged in (these can be accessed globally)
            session["user_id"] = cur.execute(f"SELECT id FROM users WHERE username = '{username}'").fetchone()[0]
            session["username"] = cur.execute(f"SELECT username FROM users WHERE username = '{username}'").fetchone()[0]
            # Once the user successfully logs in, redirect to the home page
            return [True]
        else:
            # TODO: Add warning to say that the password is INCORRECT
            message = "Password Incorrect! Try again"
            return [False, message]


def get_dash(user_id):

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        user_desc = cur.execute(f"SELECT tenure, team FROM users WHERE id = '{user_id}'").fetchall()
        levels = cur.execute(f"SELECT technology, level, experience, favourite FROM levels WHERE user_id = '{user_id}'").fetchall()
        return [levels, user_desc]

def search_users(technology):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        results = cur.execute(f"select username, forename, surname, team, levels.level, levels.experience from users INNER JOIN levels ON users.id=levels.user_id where levels.technology LIKE '{technology}' COLLATE NOCASE ORDER BY levels.level DESC").fetchall()
    return results

def get_all_users():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        results = cur.execute(f"SELECT username, forename, surname, team, tenure FROM users").fetchall()
    return results

def add_skill(user_id, technology, level, experience, favourite):
    
    liked = ""
    if favourite:
        liked = "True"
    else:
        liked = "False"
    
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO levels ('user_id', 'technology', 'level', 'experience', 'favourite') VALUES ({user_id}, '{technology}', {level}, '{experience}', '{liked}')")
        con.commit()
    return redirect('/')


def delete_skill_db(user_id, skill):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM levels WHERE user_id = {user_id} AND technology = '{str(skill)}'")
        con.commit()
    return redirect('/')