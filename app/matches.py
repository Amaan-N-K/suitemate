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
my_network = Network()


@bp.route("/get_matches", methods=["GET", "POST"])
def get_matches():
    """
    View for listing relevant matches for the logged on user.
    """
    cur_user = User(**session.get('cur_user'))
    cur_user.rent = (cur_user.rent, cur_user.rent)
    user_res = db.session.execute(db.select(model.User).where(model.User.id != cur_user.id))
    all_users = user_res.scalars()

    converted_users = find_match.convert_to_user_flask(all_users)
    for u in converted_users:
        u.rent = (u.rent, u.rent)

    parameters = decision_tree.read_file("csv_files/decision_tree_parameters.csv")
    tree = decision_tree.build_decision_tree(parameters, None)

    for u in converted_users:
        tree.add_user_to_tree(u)
    user_cluster = tree.find_exact_matches(cur_user) + [cur_user]

    my_network.create_network(user_cluster, cur_user)

    suggestions = [sugg.item for sugg in my_network.get_user(cur_user.id).suggestions]

    if request.method == 'POST':
        u1 = my_network.get_user(cur_user.id)
        other_user_id = int(request.form['other'])

        u2 = my_network.get_user(other_user_id)
        u1.send_request(u2)
        u2.accept_request(u2)

    return render_template('matches/matches.html', user_matches=suggestions)
