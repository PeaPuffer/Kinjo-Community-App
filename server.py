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
def home():
    """View homepage."""

    return render_template('home.html')


@app.route('/unofficials')
def all_unofficial():
    """View all unofficial reports"""

    unofficials = crud.view_all_unofficials()

    return render_template("all_unofficial.html", unofficials=unofficials)










if __name__=='__main__':
    connect_to_db(app)
    print("In server.py!")
    app.run(host='0.0.0.0', debug=True)