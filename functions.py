from flask import redirect, session
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
        user_pass = cur.execute(f"SELECT password FROM users WHERE username = '{username}'").fetchone()[0]
        print(f"Password: {user_pass}")

        # Now check if password matches
        if user_pass == password:
            # If the password is correct the session data is set to the user who just logged in (these can be accessed globally)
            session["user_id"] = cur.execute(f"SELECT id FROM users WHERE username = '{username}'").fetchone()[0]
            session["username"] = cur.execute(f"SELECT username FROM users WHERE username = '{username}'").fetchone()[0]
            # Once the user successfully logs in, redirect to the home page
            return redirect("/")
        else:
            # TODO: Add warning to say that the password is INCORRECT
            print("WRONG!")
    return


def get_dash(user_id):

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        levels = cur.execute(f"SELECT technology, level, experience, favourite FROM levels WHERE user_id = '{user_id}'").fetchall()
        print(levels)
        return levels

def search_users(technology):

    print(technology)
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        results = cur.execute(f"select username, forename, surname, team, levels.level, levels.experience from users INNER JOIN levels ON users.id=levels.user_id where levels.technology LIKE '{technology}' COLLATE NOCASE").fetchall()
        print(results)
    return results


def add_skill(user_id, technology, level, experience):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO levels ('user_id', 'technology', 'level', 'experience') VALUES ({user_id}, '{technology}', {level}, {experience})")
        con.commit()
    return redirect('/')


def delete_skill_db(user_id, skill):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM levels WHERE user_id = {user_id} AND technology = '{skill}'")
        con.commit()
    return redirect('/')