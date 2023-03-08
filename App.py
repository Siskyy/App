from flask import Flask, render_template, session, request, redirect, abort, jsonify
from flask_session import Session
from functions import login_required, check_credentials, get_dash, search_users, add_skill, check_for_duplicate ,delete_skill_db, get_all_users, update_skill_db
import sqlite3
import webbrowser
from threading import Timer

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'superkey'
Session(app)

# ---------------------------------------- MAIN ---------------------------------------------------

@app.route('/', methods=["GET", "POST", "DELETE"])
@login_required
def hello():
    print(session["username"])
    if request.method == "POST":
        # Check if skill already exists in table
        if check_for_duplicate(session['user_id'], request.form.get("technology")):
            return redirect('/')
        add_skill(session['user_id'], request.form.get("technology"), request.form.get("level"), request.form.get("experience"), request.form.get("favourite"))
        return redirect('/')
    elif request.method == "DELETE":
        print("deleting skill")
        return redirect('/')
    
    levels = get_dash(session["user_id"])[0]
    
    return render_template('index.html', username=session["username"], levels=levels)

# ---------------------------------------- LOGIN ---------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()
    # Check credentials of the form to see if they match with the user database
    if request.method == "POST":
        # Query database for username
        username = request.form.get("username")
        validation = check_credentials(username, request.form.get("password"))
        if validation[0]:
        # Redirect user to home page
            session["username"] = username
            session["user_id"] = validation[1]
            return redirect("/")
        else:
            return render_template("login.html", message=validation[1])
    else:
        return render_template("login.html")

# ---------------------------------------- LOGOUT ---------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------------------------------- SEARCH ---------------------------------------------------

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    
    if request.method == "POST":
        
        search_term = request.form.get("search-bar")
        if not search_term:
            user_results = get_all_users()
            search_results = ""
        else:
            search_results = search_users(search_term)
            user_results = ""
        return render_template('search.html', results=search_results, search_term=search_term, user_results=user_results)
    else:
        return render_template("search.html")

# ---------------------------------------- PROFILE ---------------------------------------------------

@app.route('/profile/<username>')
def profile(username):

    # Need to find user_id from username
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        user_id = cur.execute(f"SELECT id FROM users WHERE username = '{username}'").fetchone()[0]

    data = get_dash(user_id)
    levels = data[0]
    user_desc = data[1]
    return render_template('profile.html', username=username, levels=levels, user_desc=user_desc)

# ---------------------------------------- DELETE SKILL ---------------------------------------------------
@app.route('/delete-skill/<skill>', methods=["GET", "POST"], endpoint="delete_skill")
@login_required
def delete_skill(skill):
    if request.method == "POST":
        delete_skill_db(session["user_id"], skill)
        return redirect('/')
    else:
        return render_template('delete-skill.html', skill=skill)

# ---------------------------------------- UPDATE SKILL ---------------------------------------------------

@app.route('/update-skill/<skill>', methods=["GET", "POST"], endpoint='update_skill')
@login_required
def update_skill(skill):
    if request.method == "POST":
        print(skill)
        print(request.form.get("level"))
        print(request.form.get("experience"))
        print(request.form.get("favourite"))
        print("Excecuting update")
        if request.form.get("level") and request.form.get("experience"):
            if request.form.get("technology"): 
                fav = True 
            else: 
                fav = False
            print("LETS GO")
            update_skill_db(session['user_id'], skill, request.form.get("level"), request.form.get("experience"), fav)
            return redirect('/')
        else:
            render_template('update-skill.html', skill=skill)
    else:
        return render_template('update-skill.html', skill=skill)

def open_tab():
    webbrowser.open_new("http://127.0.0.1:2000")


if __name__ == '__main__':
    Timer(1, open_tab).start()
    app.run(port=2000)