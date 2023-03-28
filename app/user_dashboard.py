import numpy as np
from flask import Flask, render_template
from user import User
from python_ta.contracts import check_contracts

@check_contracts
def check_matches(matches: list[User]) -> None:
    pass


def update_gender_pref(user: User, info: str) -> None:
    """
    Updates user's gender preferences
    """
    user.gender_pref = info


def update_smoke(user: User, info: str) -> None:
    """
    Updates user's smoking preferences
    """
    user.smoke = info


def update_rent(user: User, info: tuple[float, float]) -> None:
    """
    Updates user's rent preferences
    """
    user.rent = info


def update_pets(user: User, info: bool) -> None:
    """
    Updates user's pets preferences
    """
    user.pets = info


def update_contact(user: User, info: str) -> None:
    """
    Updates user's contact information
    """
    user.contact = info


def update_noise(user: User, info: int) -> None:
    """
    Updates user's noise preferences
    """
    user.noise = info


def update_pets(user: User, info: bool) -> None:
    """
    Updates user's pets preferences
    """
    user.pets = info


def update_guests(user: User, info: int) -> None:
    """
    Updates user's guests preferences
    """
    user.guests = info #may be bool and not int


def update_cleanliness(user: User, info: int) -> None:
    """
    Updates user's cleanliness preferences
    """
    user.cleanliness = info


def update_roommates(user: User, info: int) -> None:
    """
    Updates user's wanted room mates preferences
    """
    user.roommates = info #spelling
