"""CRUD operations"""

from model import db, User, Unofficial, Official, Comment#, connect_to_db
from datetime import datetime
from flask import session


### USER #################################################################

def create_user(fname, lname, email, password, neighborhood):
    """Create and return new user"""

    user = User(fname=fname, 
                lname=lname, 
                email=email, 
                password=password, 
                neighborhood=neighborhood)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all users"""

    return User.query.all()

   
def get_user_by_id(user_id):
    """Return user by primary key"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """ Return a user by email"""

    return User.query.filter(User.email==email).first()

def view_all_users():
    """View all users"""

    return User.query.all()



### UNOFFICIAL ###########################################################

def create_unofficial(title, incident, created_on, neighborhood, incident_datetime, user):
    """Create and return unofficial report"""

    unofficial = Unofficial(title=title,
                    incident=incident,
                    created_on=datetime.now(),
                    neighborhood=neighborhood,
                    incident_datetime=incident_datetime,
                    user=user)

    db.session.add(unofficial)
    db.session.commit()

    return unofficial


def view_all_unofficials():
    """View all unofficial reports"""

    return Unofficial.query.all()    


def get_unofficial_by_id():
    """Get details on a unofficial report by primary key"""

    return Unofficial.query.get(unofficial_id)


### OFFICIAL #############################################################

def get_official(title, description, incident_datetime, neighborhood):
    """Get and return official report"""

    official = Official(title=title,
                        description=description,
                        incident_datetime=incident_datetime,
                        neighborhood=neighborhood)

    db.session.add(official)
    db.session.commit()

    return official        
              

def view_all_officials():
    """View all official reports"""

    return Official.query.all()


### COMMENT ##############################################################

def create_comment(content, created_on, user, official_id, unofficial_id):
    """Create and return user comment"""

    comment = Comment(content=content,
                created_on=datetime.now(),
                user=user,
                official=official,
                unofficial=unofficial)

    db.session.add(unofficial)
    db.session.commit()

    return comment







# if __name__ == '__main__':
#     from server import app
#     connect_to_db(app)