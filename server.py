"""Server for community watch app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'dev'
API_KEY = os.environ['DATASF']

app.jinja_env.undefined=StrictUndefined
connect_to_db(app)



### HOMEPAGE ##################################################

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)   


### USER REGISTRATION #########################################

@app.route('/register')
def register():
    """New user registration form"""

    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register_user():
    """Register new user"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    neighborhood = request.form.get('neighborhood')

    new_user = crud.get_user_by_email(email)
    if new_user:
        flash(f"This email is already in use. Please try a different email.")
        return redirect('/register')
    else:
        crud.create_user(fname, lname, email, password, neighborhood)
        flash(f"Successfully Registered!")

    return redirect('/')


### UNOFFICIAL REPORTS #########################################

@app.route('/unofficials')
def all_unofficial():
    """View all unofficial reports"""

    unofficials = crud.view_all_unofficials()

    return render_template("all_unofficial.html", unofficials=unofficials)


@app.route('/unofficials/<unofficial_id>')
def get_unofficial(unofficial_id):
    """Get details of a unofficial reports"""

    unofficial = crud.get_unofficial_by_id(unofficial_id)

    return render_template('unofficial_details.html', unofficial=unofficial)


@app.route('/user_incident')
def user_incident():
    """User unofficial incident report"""

    return render_template('incident_report.html', unofficial=unofficial)


@app.route('/incident_report', methods=["POST"])
def new_incident():
    """Creating a new unofficial report"""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash(f'Please log in to submit an incident')
    
    else: 
        user = crud.get_user_by_email(logged_in_email)
        # unofficial = crud.

    
    return redirect('/unofficials')


### OFFICIAL REPORTS ###########################################

@app.route('/officials')
def all_official():
    """View all official reports"""

    officials = crud.view_all_officials()

    return render_template("all_official.html", officials=officials)


### LOGIN #####################################################

@app.route("/login", methods=["POST"])
def login():
    """User login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash(f"There was an error with your email and/or password. Please try again.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    
    # return redirect('/profile')
    return redirect('/')


### LOGOUT ####################################################
 
@app.route('/logout')
def logout():
    """User logout"""
    print(session)

    if session['user_id']:
        session.pop('user_id')
        flash(f"You have successfully logged out.")
    else:
        flash(f"Please Login")
    return redirect("/")





if __name__=='__main__':
    connect_to_db(app)
    print("In server.py!")
    app.run(host='0.0.0.0', debug=True)