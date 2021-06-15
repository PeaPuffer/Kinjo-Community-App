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
with open('data/official.json') as f:
    official_data=json.loads(f.read())