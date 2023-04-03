"""
CSC111 Winter 2023 Final Project: suitemate

Derek Huynh, James Yung, Andrew Xie, Amaan Khan

================================================

A module for defining helper functions that aid in working with the SQLAlchemy database
"""
from python_ta.contracts import check_contracts
from user import User
import social_graph
import model

# @check_contracts
def convert_to_user_flask(users: list[model.User]) -> list[User]:
    """
    Converts from a list of results from a SQLAlchemy query to a list
    of custom user dataclasses
    """
    all_users = [convert_to_user_single(u) for u in users]
    return all_users


# @check_contracts
def convert_to_user_single(user: model.User) -> User:
    """
    Helper function that converts a sngle instance of a resulting SQLAlchemy query
    to an instance of a custom User dataclass
    """
    ret = User(name=user.name, 
             username=user.username, 
             id=user.id,
             age=user.age,
             rent=user.rent, 
             gender=user.gender,
             gender_pref=bool(user.gender_pref),
             smoke=bool(user.smoke),
             pets=bool(user.pets),
             contact=user.contact,
             location=user.location,
             noise=user.noise,
             guests=user.guests, 
             cleanliness=user.cleanliness,
             num_roommates=user.num_roommates
    )

    return ret

if __name__ == '__main__':
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['user', '__init__'],
        'disable': ['abstract-method', 'unused-import']
    })
