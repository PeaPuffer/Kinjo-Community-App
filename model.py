""" Models for community watch app"""

from flask_sqlalchemy import SQLALCHEMY
from datetime import datetime

db = SQLalchemy()



class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True)
    
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} fname={self.fname} city={self.city}>'



class Report(db.Model):
    """A report"""

    __tablename__ = 'reports'

    report_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    report_content = db.Column(db.Text, nullable=False)
    location = db.Column(db.String, nullable=False)
    created_report = db.Column(db.DateTime)
    #comment = db.Column(db.String(100))


    def __repr__(self):
        return f'<Report report_id={self.report} location={self.location} created_report={self.created_report}

 
 





def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')



if __name__ == '__main__':
    from server import app

    connect_to_db(app)




