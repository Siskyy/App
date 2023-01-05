from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from functions import login_required, check_credentials, search_film, get_dash, search_users
import sqlite3

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'superkey'
Session(app)

# ---------------------------------------- MAIN ---------------------------------------------------

@app.route('/')
@login_required
def hello():
    print(session["username"])
    levels = get_dash(session["user_id"])
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
        check_credentials(username, request.form.get("password"))
        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")

# ---------------------------------------- LOGOUT ---------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
# ---------------------------------------- SIGN UP ---------------------------------------------------
@app.route("/signup")
def signup():
    return redirect("/")

# ---------------------------------------- SEARCH ---------------------------------------------------

@app.route('/search', methods=["GET", "POST"])
def search():
    
    if request.method == "POST":
        
        search_term = request.form.get("search-bar")
        print(f"Search term: {search_term}")
        search_results = search_users(search_term)
        

        return render_template('search.html', results=search_results, search_term=search_term)
    
    else:
        return render_template("search.html")

# ---------------------------------------- RANKINGS ---------------------------------------------------
@app.route('/rankings')
def rankings():
    
    user_id = 0
    # Get the ranked films and save them to a variable
    with sqlite3.connect("rankings.db") as con:
        cur = con.cursor()
        ranked_films = cur.execute(f"SELECT * FROM '{user_id}_rankings' ORDER BY ranking ASC")
    print(ranked_films)
    
    
    
    
    return render_template("rankings.html") # , films = ranked_films (so that the list of films can be displayed later on html file)



if __name__ == '__main__':
    app.run()


# ---------------------------------------- DASHBOARD ---------------------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():

    return render_template("dashboard.html")