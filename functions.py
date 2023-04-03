from flask import redirect, session
from functools import wraps
import sqlite3
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s - %(message)s')

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
def check_credentials(username: str, password: str):
    # First check the username in the database
    with sqlite3.connect("database.db") as con: # connects to the database
        cur = con.cursor()
        # Checks wether there is a password for the username inputted by the user
        # If the user enters a username that does not exist, a password will not be found
        user_pass = cur.execute(f"SELECT password FROM users WHERE username = '{username}'").fetchone()
        if user_pass == None:
            message = f"User '{username}' does not exist!"
            logging.error("404 - Username not found")
            return [False, message]
        else:
            user_pass = user_pass[0]

        # Now check if password matches
        if user_pass == password:
            # Set session data to logged in user
            user_id = cur.execute(f"SELECT id FROM users WHERE username = '{username}'").fetchone()[0]
            # Once the user successfully logs in, redirect to the home page
            return [True, user_id]
        else:
            message = "Password Incorrect! Try again"
            logging.error("403 - Password Incorrect")
            return [False, message]


def get_dash(user_id: str):

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        user_desc = cur.execute(f"SELECT tenure, team FROM users WHERE id = '{user_id}'").fetchall()
        levels = cur.execute(f"SELECT technology, level, experience, favourite FROM levels WHERE user_id = '{user_id}'").fetchall()
        return [levels, user_desc]

def search_users(technology: str):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        results = cur.execute(f"""select 
            username, forename, surname, team, levels.level, levels.experience 
            from users INNER JOIN levels ON users.id=levels.user_id 
            where levels.technology LIKE '{technology}' COLLATE NOCASE ORDER BY levels.level DESC""").fetchall()
        if not results:
            logging.info("404 - No users found")
    return results

def get_all_users():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        results = cur.execute(f"SELECT username, forename, surname, team, tenure FROM users").fetchall()
        if results:
            logging.error("409 - Skill already exists")
    return results

def check_for_duplicate(user_id: str, technology: str):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        dupes = cur.execute(f"SELECT technology FROM levels WHERE user_id = '{user_id}' AND technology = '{technology}'").fetchall()
    return dupes

def add_skill(user_id: str, technology: str, level, experience: str, favourite):
    
    liked = ""
    if favourite:
        liked = "True"
    else:
        liked = "False"
    
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO levels ('user_id', 'technology', 'level', 'experience', 'favourite') VALUES ({user_id}, '{technology}', {level}, '{experience}', '{liked}')")
        con.commit()
    return 200


def delete_skill_db(user_id, skill):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM levels WHERE user_id = {user_id} AND technology = '{str(skill)}'")
        con.commit()
    return 200

def update_skill_db(user_id, technology, level, experience, favourite):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE levels SET level = '{level}', experience = '{experience}', favourite = '{favourite}' WHERE technology = '{technology}' AND user_id = '{user_id}'")
        con.commit()

    return 200