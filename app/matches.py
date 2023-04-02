import decision_tree
import random
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

parameters = decision_tree.read_file("csv_files/decision_tree_parameters.csv")
tree = decision_tree.build_decision_tree(parameters, None)


@bp.route("/get_matches", methods=["GET", "POST"])
def get_matches():
    """
    View for listing relevant matches for the logged on user.
    """
    cur_user = User(**session.get('cur_user'))
    cur_user.rent = (cur_user.rent, cur_user.rent)
    user_res = db.session.execute(db.select(model.User).where(model.User.id != cur_user.id))
    #user_res = db.session.execute(db.select(model.User).order_by(model.User.id))
    all_users = user_res.scalars()

    converted_users = find_match.convert_to_user_flask(all_users)

    for u in converted_users:
        u.rent = (u.rent, u.rent)

    if tree.users is None:
        for u in converted_users:
            tree.add_user_to_tree(u)

    tree.add_user_to_tree(cur_user)
    communities = tree.find_all_leaves()

    my_network.create_network_all(communities, cur_user, 500)

    # cur_user = User(**session.get('cur_user'))
    # cur_user.rent = (cur_user.rent, cur_user.rent)
    # user_res = db.session.execute(db.select(model.User).where(model.User.id != cur_user.id))
    # all_users = user_res.scalars()

    # converted_users = find_match.convert_to_user_flask(all_users)

    # user_cluster = tree.find_exact_matches(cur_user) + [cur_user]

    # my_network.create_network_single_community(user_cluster, cur_user)

    suggestions = [sugg.item for sugg in my_network.get_user(cur_user.id).suggestions]

    if suggestions == []:
        my_network.random_suggestion_user(cur_user) # add atleast one random suggestion
    else:
        if random.choice([True, False]):
            my_network.random_suggestion_user(cur_user)

        suggestions = [sugg.item for sugg in my_network.get_user(cur_user.id).suggestions]

    if request.method == 'POST':
        u1 = my_network.get_user(cur_user.id)
        other_user_id = int(request.form['other_id'])

        u2 = my_network.get_user(other_user_id)

        if u2.item not in suggestions:
            suggestions.append(u2.item)

        my_network.add_suggestion(u2.item, u1.item)
        u1.send_request(u2)
        u2.accept_request(u1)

        match_msg = "Successful match"
        flash(match_msg)

        suggestions.remove(u2.item)

    return render_template('matches/matches.html', user_matches=suggestions)


@bp.route("/current_matches", methods=["GET", "POST"])
def current_matches():
    cur_user = User(**session.get('cur_user'))

    node = my_network.get_user(cur_user.id)
    if node is not None:
        cur_user_matches = [sugg.item for sugg in node.matches]
    else:
        cur_user_matches  = []

    return render_template('matches/current_matches.html', cur_user_matches=cur_user_matches)

@bp.route("/community", methods=["GET", "POST"])
def community():
    cur_user = User(**session.get('cur_user'))

    node = my_network.get_user(cur_user.id)
    if node is not None:
        _, cur_community = node.find_all_connected_matches(set())
        cur_community = [comm.item for comm in cur_community]
    else:
        cur_community = []

    return render_template('matches/community.html', cur_community=cur_community)
