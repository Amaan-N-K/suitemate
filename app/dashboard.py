"""
Creating the dashboard for a given user with options to edit their profile/preferences
and to find roommate matches as well as look at their previously liked matches

TODO:
    - CRUD capability for updating images
    - Add an upload feature for images
"""
from flask import (
    g, session, request, Blueprint, redirect, render_template, flash, url_for
)
#from ocularnn.db import get_db
from __init__ import db
from auth import requires_auth

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template("dashboard/dashboard.html")
