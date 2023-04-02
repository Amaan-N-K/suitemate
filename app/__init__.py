import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    # from . import auth
    import auth
    app.register_blueprint(auth.bp)

    #from . import dashboard
    import dashboard
    app.register_blueprint(dashboard.bp)

    import matches
    app.register_blueprint(matches.bp)

    def main_template():
        return render_template('base.html')

    app.add_url_rule('/', endpoint='home', view_func=main_template)

    # from . import model

    with app.app_context():
        db.create_all()

    return app
