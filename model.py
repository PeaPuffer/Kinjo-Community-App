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
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    neighborhood = db.Column(db.String, nullable=False)

    #comments = a list of Comment objects (db.relationship)


    def __repr__(self):
        """Show info about user"""
        return f"<User user_id={self.user_id} email={self.email} fname={self.fname} neighborhood={self.neighborhood}>"



class Official(db.Model):
    """A official report"""

    __tablename__ = "officials"

    official_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_datetime = db.Column(db.DateTime, nullable=False) #when did it happen
    neighborhood = db.Column(db.String, nullable=False)
    # comment_id = db.Column(db.Integer, db.ForeignKey("comments.comment_id"), nullable=True)
    
    #comments = a list of Comment objects (db.relationship)
    comment = db.relationship("Comment", backref="officials")


    def __repr__(self):
        """Show info about report"""
        return f"<Official official_id={self.official_id} title={self.title} description={self.description} incident_datetime={self.incident_datetime}>"



class Unofficial(db.Model):
    """A unofficial report"""

    __tablename__ = "unofficials"

    unofficial_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    incident = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    neighborhood = db.Column(db.String, nullable=False)
    incident_datetime = db.Column(db.DateTime, nullable=False) #don't use datetime.now()
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # comment_id = db.Column(db.Integer, db.ForeignKey("comments.comment_id"), nullable=True)
    
    #comments = a list of Comment objects (db.relationship)

    user = db.relationship("User", backref="unofficials")
    comment = db.relationship("Comment", backref="unofficials")

    def __repr__(self):
        """Show info about unofficial report"""
        return f"<Unofficial unofficial_id={self.unofficial_id} title={self.title} incident={self.incident} created_on={self.created_on} incident_datetime={self.incident_datetime} user_id={self.user_id}>"



class Comment(db.Model):
    """A comment"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    created_on =db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    official_id = db.Column(db.Integer, db.ForeignKey("officials.official_id"))
    unofficial_id = db.Column(db.Integer, db.ForeignKey("unofficials.unofficial_id"))

    user = db.relationship("User", backref="comments")
    # unofficial = db.relationship("Unofficial", backref="comments")
    # official = db.relationship("Official", backref="comments")


    def __repr__(self):
        """Show comments"""
        return f'<Comment comment_id={self.comment_id} content={self.content} created_on={self.created_on} user_id={self.user_id} unofficial={self.unofficial_id} official={self.official_id}>'




def connect_to_db(flask_app, db_uri='postgresql:///reports', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')



if __name__ == '__main__':
    from server import app
    print("We're in model.py file")
    connect_to_db(app)




