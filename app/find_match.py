"""
find match
"""
from __future__ import annotations
from python_ta.contracts import check_contracts
from typing import Optional
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import create_engine, select, Column, Integer, String, Boolean, Float
from user import User as Us
from user import generate_random_users
import social_graph
import model

class Base(DeclarativeBase):
    pass

class UserDB(Base):
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
    __tablename__ = 'users_db'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    contact = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    gender_pref = Column(Boolean)
    smoke = Column(Boolean)
    rent = Column(Float)
    pets = Column(Boolean)
    location = Column(String)
    noise = Column(Integer)
    guests = Column(Integer)
    cleanliness = Column(Integer)
    num_roommates = Column(Integer)

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

def convert_to_model(user: Us) -> UserDB:
    """
    Given a user from the original user.py file, return the equivalent User db model.
    """
    new_id = user.id
    new_username = user.username
    new_pass = "abc123"
    new_name = user.name
    new_contact = user.contact
    new_age = user.age
    new_gender = user.gender
    new_gender_pref = user.gender_pref
    new_smoke = user.smoke
    new_rent = user.rent[0]
    new_pets = user.pets
    new_location = f"{user.location[0]}, {user.location[1]}"
    new_noise = user.noise
    new_guests = user.guests
    new_cleanliness = user.cleanliness
    new_num_roommates = user.num_roommates

    new_user = UserDB(id=new_id, username=new_username, password=new_pass, name=new_name, contact=new_contact, age=new_age,
                      gender=new_gender, gender_pref=new_gender_pref, smoke=new_smoke,
                    rent=new_rent, pets=new_pets, location=new_location, noise=new_noise, guests=new_guests, cleanliness=new_cleanliness, num_roommates=new_num_roommates)

    return new_user


def convert_and_write(users: list[Us]) -> None:
    """
    given users, add it to the database
    """
    with Session(engine) as session:
        for u in users:
            user_res = select(UserDB).where(UserDB.id == u.id)
            user_info = session.scalars(user_res).one_or_none()
            if user_info is None:
                entry = convert_to_model(u)
                session.add(entry)
                session.commit()

def convert_to_user(eng) -> list[Us]:
    """
    conver user
    """
    with Session(eng) as session:
        accum = []
        stmt = select(UserDB).where(UserDB.id >= 1)
        for user in session.scalars(stmt):
            u = Us(name=user.name, username=user.username, id=user.id, age=user.age, gender=user.gender,
                   gender_pref=user.gender_pref, smoke=user.smoke, pets=user.pets,
                   contact=user.contact, location=user.location, noise=user.noise, guests=user.guests,
                   cleanliness=user.cleanliness, num_roommates=user.num_roommates)

            accum.append(u)
        return accum

def convert_to_user_flask(users: list[model.User]) -> list[Us]:
    """
    conver user
    """
    all_users = [convert_to_user_single(u) for u in users]
    return all_users

def convert_to_user_single(user: model.User) -> Us:
    """
    conver user
    """
    ret = Us(name=user.name, username=user.username, id=user.id, age=user.age, rent=user.rent,
           gender=user.gender, gender_pref=user.gender_pref, smoke=user.smoke, pets=user.pets,
           contact=user.contact, location=user.location, noise=user.noise, guests=user.guests,
           cleanliness=user.cleanliness, num_roommates=user.num_roommates)

    return ret


if __name__ == '__main__':
    list_users = generate_random_users('csv_files/names.csv', 1000)
    convert_and_write(list_users)
