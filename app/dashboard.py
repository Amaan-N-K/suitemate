"""
Creating the dashboard for a given user with options to view their profile/preferences
and to find roommate matches as well as look at their previously liked matches.
"""
from flask import (
    g, session, request, Blueprint, redirect, render_template, flash, url_for
)
from __init__ import db
from auth import requires_auth

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template("dashboard/dashboard.html")
