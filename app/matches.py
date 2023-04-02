import decision_tree
import find_match
from flask import (
    g, session, request, Blueprint, redirect, render_template, flash, url_for, abort
)
from . import db
from app.model import User
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

bp = Blueprint("matches", __name__, url_prefix="/matches")

users = db.session.execute(db.select(User).order_by(User.username)).scalars()
converted_users = find_match.convert_to_user(users)
user_preferences = decision_tree.get_user_preferences(converted_users)
tree = decision_tree.build_decision_tree(user_preferences)


@bp.route("/get_match", methods=["GET", "POST"])
def get_match():
    """
    View for finding relevant matches for the logged on user.
    """
    user_res = db.session.execute(db.select(User).where(User.username == username))
    user_info = user_res.one_or_none()
