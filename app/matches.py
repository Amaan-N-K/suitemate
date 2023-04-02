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
from main import create_network
from social_graph import Network, _User
from functools import wraps

bp = Blueprint("matches", __name__, url_prefix="/matches")
@bp.route("/get_matches", methods=["GET", "POST"])
def get_matches():
    """
    View for listing relevant matches for the logged on user.
    """
    cur_user = User(**session.get('cur_user'))
    cur_user.rent = (cur_user.rent, cur_user.rent)
    #if 'tree' not in session:
    user_res = db.session.execute(db.select(model.User).where(model.User.id != cur_user.id))
    all_users = user_res.scalars()


    converted_users = find_match.convert_to_user_flask(all_users)
    for u in converted_users:
        u.rent = (u.rent, u.rent)

    #user_preferences = decision_tree.get_users_preferences(converted_users)

    parameters = decision_tree.read_file("csv_files/decision_tree_parameters.csv")
    tree = decision_tree.build_decision_tree(parameters, None)

    for u in converted_users:
        tree.add_user_to_tree(u)

        #session['tree'] = tree

    #tree = session['tree']
    user_cluster = tree.find_exact_matches(cur_user) + [cur_user]
    #print("suggestions", user_suggestions)
    my_network = Network()
    my_network.create_network(user_cluster)

    suggestions = [sugg.item for sugg in my_network.get_user(cur_user.id).suggestions]

    return render_template('matches/matches.html', user_matches=suggestions)
