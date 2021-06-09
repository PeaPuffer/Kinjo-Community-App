""" Models for community watch app"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True)
    
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    u_neighborhood = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email} fname={self.fname}>"



class Report(db.Model):
    """A report"""

    __tablename__ = "reports"

    report_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    report_title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    report_datetime = db.Column(db.DateTime, nullable=False)
    neighborhood = db.Column(db.String, nullable=False)
    user_report_id = db.Column(db.Integer, db.ForeignKey("user_reports.user_report_id"))




    def __repr__(self):
        return f"<Report report_id={self.report_id} report_title={self.report_title} description={self.description} report_datetime={self.report_datetime} user_report_id={self.user_report_id}>"



class UserReport(db.Model):
    """A user report"""

    __tablename__ = "user_reports"

    user_report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_title = db.Column(db.String, nullable=False)
    incident = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    incident_datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


    def __repr__(self):
        return f"<UserReport incident_title={self.incident_title} incident={self.incident} incident_datetime={self.incident_datetime} user_id{self.user_id}>"



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




