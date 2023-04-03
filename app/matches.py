"""
CSC111 Winter 2023 Final Project: suitemate

Derek Huynh, James Yung, Andrew Xie, Amaan Khan

================================================

A collection of flask views that are responsible for displaying the simulation
of finding suite mate matches. Does this via a decision tree and tracking the matches
with a global social graph. We recommend users their closest matches via a decision
tree that specifically filters for the user's desired qualities. Additionally, we use
path finding algorithms over our graph to store the relationships between users, one 
set of edges representing the suggestions and another the mutual matches.
"""
import decision_tree
import random
from flask import (
    g, session, request, Blueprint, redirect, render_template, flash, url_for
)
from __init__ import db
import model
from sqlalchemy.exc import IntegrityError
from user import User
from main import create_network
from social_graph import Network, _User
from auth import requires_auth

bp = Blueprint("matches", __name__, url_prefix="/matches")
my_network = Network()

parameters = decision_tree.read_file("csv_files/decision_tree_parameters.csv")
tree = decision_tree.build_decision_tree(parameters, None)


def convert_to_user_flask(users: list[model.User]) -> list[User]:
    """
    Converts from a list of results from a SQLAlchemy query to a list
    of custom user dataclasses
    """
    all_users = [convert_to_user_single(u) for u in users]
    return all_users


def convert_to_user_single(user: model.User) -> User:
    """
    Helper function that converts a sngle instance of a resulting SQLAlchemy query
    to an instance of a custom User dataclass
    """
    ret = User(name=user.name, 
             username=user.username, 
             id=user.id,
             age=user.age,
             rent=user.rent, 
             gender=user.gender,
             gender_pref=bool(user.gender_pref),
             smoke=bool(user.smoke),
             pets=bool(user.pets),
             contact=user.contact,
             location=user.location,
             noise=user.noise,
             guests=user.guests, 
             cleanliness=user.cleanliness,
             num_roommates=user.num_roommates
    )

    return ret


@requires_auth
@bp.route("/get_matches", methods=["GET", "POST"])
def get_matches():
    """
    View for listing relevant suitemate matches for the logged on user.
    """
    cur_user = User(**session.get('cur_user'))
    cur_user.rent = (cur_user.rent, cur_user.rent)
    user_res = db.session.execute(db.select(model.User).where(model.User.id != cur_user.id))
    all_users = user_res.scalars()

    converted_users = convert_to_user_flask(all_users)

    for u in converted_users:
        u.rent = (u.rent, u.rent)

    if tree.users is None:
        for u in converted_users:
            tree.add_user_to_tree(u)

    tree.add_user_to_tree(cur_user)
    communities = tree.find_all_leaves()

    my_network.create_network_all(communities, cur_user, 500)

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


@requires_auth
@bp.route("/current_matches", methods=["GET", "POST"])
def current_matches():
    """
    View for displaying the current matches that the user has performed
    """
    cur_user = User(**session.get('cur_user'))

    node = my_network.get_user(cur_user.id)
    if node is not None:
        cur_user_matches = [sugg.item for sugg in node.matches]
    else:
        cur_user_matches  = []

    return render_template('matches/current_matches.html', cur_user_matches=cur_user_matches)


@requires_auth
@bp.route("/community", methods=["GET", "POST"])
def community():
    """
    The "community" surrounding the given current user, which is the
    set of all users that are connected by a mutual "match".
    """
    cur_user = User(**session.get('cur_user'))

    node = my_network.get_user(cur_user.id)
    if node is not None:
        _, cur_community = node.find_all_connected_matches(set())
        cur_community = [comm.item for comm in cur_community]
    else:
        cur_community = []

    return render_template('matches/community.html', cur_community=cur_community)

if __name__ == '__main__':
    import python_ta
    
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['flask', 'decision_tree', 'random', 'model', 
                          'sqlalchemy', 'user', 'main', 'social_graph', 'auth']
    })
