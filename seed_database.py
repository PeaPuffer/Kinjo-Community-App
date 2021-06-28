"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb reports')
os.system('createdb reports')

model.connect_to_db(server.app)
model.db.create_all()

#Load official report data from json file
# with open('data/official.json') as f:
#     official_data=json.loads(f.read())


# official_in_db = []
# for official in official_data:
#     title, description, incident_datetime_neighborhood = (
#         official["title"],
#         official["description"],
#         #official["incident_datetime"],
#         official["neighborhood"],
#     )

#     incident_datetime = datetime.strptime(official["incident_datetime"], "%Y-%m-%d")

#     db_official = crud.get_official(title, description, incident_datetime, neighborhood)
#     official_in_db.append(db_official) 


### SEED USERS ##########################################################

#neighborhood = ["Richmond", "Mission Bay", "Sunset", "Bernal Heights", "Forest Hill", "Sea Cliff"]

for n in range(10):
    fname = f'Rubber{n}'
    lname = f'Duck{n}'
    email = f'user{n}@test.com'
    password = 'test'
    neighborhood = 'Richmond' #choice(neighborhood)

    user = crud.create_user(fname, lname, email, password, neighborhood)


### KUCHI KOPI'S ACCOUNT ################################################

crud.create_user("Kuchi", "Kopi", "kuchikopi@bobsburgers.com", "kk123", "Fortress")

### SEED UNOFFICIAL REPORTS #############################################

