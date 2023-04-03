"""
CSC111 Winter 2023 Final Project: suitemate

Derek Huynh, James Yung, Andrew Xie, Amaan Khan

================================================

This module is where we create our flask app which is responsible for serving all of our api endpoints
and is used for all of flask modules and defining our SQLAlchemy database. Here we also generate a
synthetic dataset of users and do a mass insertion into our database. You can edit the number of users
inserted into the data base to scale your simulation. We found that 20,000 was a reasonable number.

Comment out check contracts to generate users more quickly.
"""

import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from python_ta.contracts import check_contracts
import model

db = SQLAlchemy()


# @check_contracts
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Setting configs
    app.config.from_mapping({
        "SECRET_KEY": "dev",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///suitemate.db"
    })

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py", silent=True)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # Registering database initialization
    db.init_app(app)

    from user import generate_random_users

    @app.before_first_request
    def generate_users_and_insert_into_db():
        # Clear the db after opening up a new session
        db.session.query(model.User).delete()
        db.session.commit()

        # Feel free to edit the number of users to generate
        list_users = generate_random_users('csv_files/names.csv', 20000)
        entry = []
        for u in list_users:
            converted = model.convert_to_model(u)
            entry.append(converted)
        db.session.add_all(entry)
        db.session.commit()

    import auth
    app.register_blueprint(auth.bp)

    import dashboard
    app.register_blueprint(dashboard.bp)

    import matches
    app.register_blueprint(matches.bp)

    def main_template():
        return render_template('base.html')

    app.add_url_rule('/', endpoint='home', view_func=main_template)

    with app.app_context():
        db.create_all()

    return app
