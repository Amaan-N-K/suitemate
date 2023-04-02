"""
find match
"""
from __future__ import annotations
from python_ta.contracts import check_contracts
from typing import Optional

from . import db
from user import User as Us
import social_graph
from model import User


def convert_to_user() -> list[User]:
    """
    conver user
    """
    users = db.session.query(User).all()
    accum = []
    for user in users:

        u = Us(user.name, user.username, user.id, user.age, user.gender, user.gender_pref, user.smoke, user.pets,
               user.contact, user.location, user.noise, user.guests, user.cleanliness, user.num_roommates)

        accum.append(u)
    return accum
