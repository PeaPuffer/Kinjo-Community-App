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


def get_unofficial(unofficial_id):
    """ """
    return Unofficial.query.filter(Unofficial.unofficial_id == unofficial_id).first()


def view_all_unofficials():
    """View all unofficial reports"""

    return Unofficial.query.all()    


def get_unofficial_by_id(unofficial_id):
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


###** OFFICIAL API SEARCH **#########

def get_official_report():
    """Return titles of official report"""

    officials = Official.query.all()
    official_titles = []

    for official_title in officials:
        official_titles.append(official.title)
    
    return official_titles










### COMMENT ##############################################################

def create_comment(content, created_on, user_id, unofficial_id):
    """Create and return user comment"""

    u_comment = Comment(content=content,
                created_on=datetime.now(),
                user_id=user_id,
                unofficial_id=unofficial_id)

    db.session.add(u_comment)
    db.session.commit()

    return u_comment


def get_comments_by_unofficial_id(unofficial_id):
    """Return user comment in unofficial reports"""

    return Comment.query.filter(Comment.unofficial_id == unofficial_id).all()


def delete_comment(user_id, comment_id):
    """Delete user comment"""

    u_comment = (Comment.query.filter(Comment.user_id == user_id).filter(Comment.comment_id == comment_id).first())

    db.session.delete(u_comment)
    db.session.commit()
    








# if __name__ == '__main__':
#     from server import app
#     connect_to_db(app)