import decision_tree
import find_match
from flask import (
    g, session, request, Blueprint, redirect, render_template, flash, url_for, abort
)
from __init__ import db
import model
from sqlalchemy.exc import IntegrityError
from find_match import convert_to_user_flask
from user import User

from functools import wraps

bp = Blueprint("matches", __name__, url_prefix="/matches")

@bp.route("/get_matches", methods=["GET", "POST"])
def get_matches():
    """
    View for listing relevant matches for the logged on user.
    """
    cur_user = User(**session.get('cur_user'))
    if 'tree' not in session:
        user_res = db.session.execute(db.select(model.User).where(model.User.id != cur_user.id))
        all_users = user_res.scalars()

        print(all_users)

        converted_users = find_match.convert_to_user_flask(all_users)
        user_preferences = decision_tree.get_user_preferences(converted_users)
        tree = decision_tree.build_decision_tree(user_preferences)

        for u in all_users:
            tree.add_user_to_tree(u)

        session['tree'] = tree
    else:
        tree = session['tree']
        user_matches = tree.find_exact_matches(cur_user)

    return render_template('matches/matches.html', user_matches=user_matches)
