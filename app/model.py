from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from . import db

class User(db.Model):
    """
    A custom data type that represents each user
    Instance Attributes:
        - name: The name of the user
        - username: the user's username (log in credentials)
        - id: unique integer identifier for each user
        - age: the age of the user
        - gender: the gender of the user
        - gender_pref: prefered gender of user's roomates
        - smoke: whether user is fine with a smoking environment
        - rent: price range the user is willing to pay monthly
        - pets: whether user is fine with having pets in the place
        - contact: contact information of user
        - location: country and city the user wants to find a place in
        - noise: noise level the user is comfortable with
        - guests: whether user is fine with having guests
        - cleanliness: cleanliness preference of the user
        - num_roommates: number of roomates the user is looking for (e.g. 1, 2, 3, 4+)
    Representation Invariants:
        - 17 <= self.age <= 100
        - 1 <= self.num_roommates <= 100
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    contact = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    gender_pref = db.Column(db.Boolean)
    smoke = db.Column(db.Boolean)
    rent = db.Column(db.Float)
    pets = db.Column(db.Boolean)
    location = db.Column(db.String)
    noise = db.Column(db.Integer)
    guests = db.Column(db.Integer)
    cleanliness = db.Column(db.Integer)
    num_roommates = db.Column(db.Integer)
