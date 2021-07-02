"""Server for community watch app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
import os
import requests

app = Flask(__name__)

app.secret_key = 'dev'
API_KEY = os.environ['DATASF_KEY']

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

    return redirect('/login')

@app.route('/profile')
def profile():
    """User profile"""

    return render_template('profile.html') #saved_neighbhorhoood.html or saved_unofficial/official


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
    comments = crud.get_comments_by_unofficial_id(unofficial_id)

    return render_template('unofficial_details.html', unofficial=unofficial, comments=comments)


@app.route('/incident_report')
def user_incident():
    """User unofficial incident report"""

    return render_template('incident_reports.html')


@app.route('/incident_report', methods=["POST"])
def new_incident():
    """Creating a new unofficial report"""

    logged_in_email = session.get("user_email")
    

    title = request.form.get("title")
    incident = request.form.get("incident")
    created_on = request.form.get("created_on")
    neighborhood = request.form.get("neighborhood")
    incident_datetime = request.form.get("incident_datetime")

    
    if logged_in_email is None:
        flash(f'Please log in to submit an incident')
        return redirect('/')
    else: 
        user = crud.get_user_by_email(logged_in_email)
        crud.create_unofficial(title, incident, created_on, neighborhood, incident_datetime, user)
        return redirect('/unofficials')

    
    
### OFFICIAL REPORTS ###########################################

@app.route('/officials')
def all_official():
    """View all official reports"""

    officials = crud.view_all_officials()

    return render_template("all_official.html", officials=officials)


###** OFFICIAL REPORTS API **#######################################

@app.route('/search')
def display_search():

    incidents = []
    
    return render_template('search.html', incidents=incidents)


@app.route('/search', methods=['POST'])
def search_reports():
    """Search for official reports"""

    incidents = crud.get_official_report()


    print("In search route")

    url = 'https://data.sfgov.org/resource/wg3w-h783.json'
    payload = {'$$app_token': API_KEY}         
    res = requests.get(url, params=payload)
    data = res.json()

    #grab user search input #need .title()
    search = request.form.get("incident")
    print(search)
    print("*"*20)
    incident_dict = {}
    for incident in data:
        incident_dict[incident['incident_description']] = []
    incidents = []
    for incident in data:
        incidents.append(incident)
        incident_dict[ incident['incident_description'] ].append(incident)

    search_incidents = incident_dict[search]
    print('search incidents', search_incidents)
    return render_template("search.html", incidents=search_incidents)


@app.route('/official_detail/<incident_id>')
def official_detail(incident_id):
    """Search results for individual official reports"""

    url = 'https://data.sfgov.org/resource/wg3w-h783.json'
    payload = {'$$app_token': API_KEY,
                "incident_id": incident_id
    }         
    res = requests.get(url, params=payload)
    data = res.json()
    print('!'*20)
    print(data)

    return render_template('official_detail.html', incident=data[0])


### COMMENT ####################################################

@app.route("/unofficials/<unofficial_id>/comment", methods=['GET'])
def add_comment_from_unofficials(unofficial_id):

    unofficial = crud.get_unofficial(unofficial_id)
    if not unofficial:
        return redirect('/')
    
    user_id = session['user_id']
    comment = request.form.get("comment")

    crud.create_comment(content="comment", created_on=datetime.now(), user_id=user_id, unofficial_id=unofficial_id)
    return redirect(f"/unofficials/{unofficial_id}")


### LOGIN ######################################################

@app.route("/login")
def user_login():
    """Display login page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """User login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash(f"There was an error with your email and/or password. Please try again.")
        return redirect('/login')
    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.fname}!")
        return redirect('/') #change to profile when save features added


### LOGOUT ####################################################
 
@app.route('/logout')
def logout():
    """User logout"""
    print(session)

    if session['user_email']:
        session.pop('user_email')
        flash(f"You have successfully logged out.")
    else:
        flash(f"Please Login")
    return redirect("/")


if __name__=='__main__':
    connect_to_db(app)
    print("In server.py!")
    app.run(host='0.0.0.0', debug=True)