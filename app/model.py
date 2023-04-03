"""
CSC111 Winter 2023 Final Project: suitemate

Derek Huynh, James Yung, Andrew Xie, Amaan Khan

================================================

Defining the ORM for the Flask webapp using the SQLAlchemy extension to Flask.

The User class represents an abstraction of a SQL schema, which
allows us to integrate our database better with built in python objects and data types.

The User class definition relies on the db object defined in __init__.py along with the
routines for constructing the Flask app. It is a convienent extension that allows us to
access methods from SQLAlchemy without having explicitly inherit from the standard base
class from SQLAlchemy.

The classes here should not be accessed outside of a Flask app context.
"""
from __init__ import db
import user


class User(db.Model):
    """
    A custom data type that inherits from the SQLAlchemy ORM base declarative class.
    Represents an entry into a table for a user of the suitemate app.


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
        - 1 <= self.num_roommates <= 4
        - 1 <= cleanliness <= 3
        - 1 <= noise <= 3
    """
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    name: str = db.Column(db.String)
    contact: str = db.Column(db.String, nullable=False)
    age: int = db.Column(db.Integer)
    gender: str = db.Column(db.String)
    gender_pref: bool = db.Column(db.Boolean)
    smoke: bool = db.Column(db.Boolean)
    rent: float = db.Column(db.Float)
    pets: bool = db.Column(db.Boolean)
    location: str = db.Column(db.String)
    noise: int = db.Column(db.Integer)
    guests: int = db.Column(db.Integer)
    cleanliness: int = db.Column(db.Integer)
    num_roommates: int = db.Column(db.Integer)


def convert_to_model(user: user.User) -> User:
    """
    Given a user from the our custom User dataclass defined in user.py, return the
    equivalent User db model.
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
    new_rent = (user.rent[0] + user.rent[1]) // 2
    new_pets = user.pets
    new_location = f"{user.location[0]}, {user.location[1]}"
    new_noise = user.noise
    new_guests = user.guests
    new_cleanliness = user.cleanliness
    new_num_roommates = user.num_roommates

    new_user = User(
        id=new_id,
        username=new_user,
        password=new_pass,
        name=new_name,
        contact=new_contact,
        age=new_age,
        gender=new_gender,
        gender_pref=new_gender_pref,
        smoke=new_smoke,
        rent=new_rent,
        pets=new_pets,
        location=new_location,
        noise=new_noise,
        guests=new_guests,
        cleanliness=new_cleanliness,
        num_roommates=new_num_roommates
    )

    return new_user


def convert_and_write(users: list[User]) -> None:
    """
    Given users, add it to an instance of the Flask-SQLAlchemy database.

    Preconditions
        - all fields in an element in Users is valid according to the model
    """
    for user in users:
        user_res = db.session.execute(db.select(User).where(User.id == user.id))
        user_info = user_res.one_or_none()
        if user_info is not None:
            db.session.add(user_res)
            db.session.commit()


# if __name__ == '__main__':
#     import python_ta
# 
#     python_ta.check_all(config={
#         'max-line-length': 120,
#         'extra-imports': ['user', '__init__'],
#         'disable': ['abstract-method', 'unused-import']
#     })
