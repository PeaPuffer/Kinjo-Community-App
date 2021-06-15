"""Server for community watch app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined=StrictUndefined
connect_to_db(app)

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)   


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
        flash("This email has already been registered. Try another email.")
    else:
        crud.create_user(fname, lname, email, password, neighborhood)
        flash("Successfully Registered!")

    return redirect('/')


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


@app.route('/officials')
def all_official():
    """View all official reports"""

    officials = crud.view_all_officials()

    return render_template("all_official.html", officials=officials)






if __name__=='__main__':
    connect_to_db(app)
    print("In server.py!")
    app.run(host='0.0.0.0', debug=True)