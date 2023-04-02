from flask import (
    g, session, request, Blueprint, redirect, render_template, flash, url_for, abort
)
from . import db
from app.model import User
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

bp = Blueprint("matches", __name__, url_prefix="/matches")

@bp.route("/get_match", methods=["GET", "POST"])
def get_match():
    """
    View for finding relevant matches for the logged on user.
    """
