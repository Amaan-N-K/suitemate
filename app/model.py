from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from . import db
import user


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


def convert_to_model(user: user.User) -> User:
    """
    Given a user from the original user.py file, return the equivalent User db model.
    """
    new_id = user.id
    new_user = user.username
    new_pass = "abc123"
    new_name = user.name
    new_contact = user.contact
    new_age = user.age
    new_gender = user.gender
    new_gender_pref = user.gender_pref
    new_smoke = user.smoke
    new_rent = user.rent
    new_pets = user.pets
    new_location = user.location
    new_noise = user.noise
    new_guests = user.guests
    new_cleanliness = user.cleanliness
    new_num_roommates = user.num_roommates

    new_user = User(new_id, new_user, new_pass, new_name, new_contact, new_age, new_gender, new_gender_pref, new_smoke,
                    new_rent, new_pets, new_location, new_noise, new_guests, new_cleanliness, new_num_roommates)

    return new_user


def convert_and_write(users: list[User]) -> None:
    """
    given users, add it to the database
    """
    for user in users:
        user_res = db.session.execute(db.select(User).where(User.id == user.id))
        user_info = user_res.one_or_none()
        if user_info is not None:
            db.session.add(user_res)
            db.session.commit()
