"""
    This module is responsible for creating the Flask app instance and registering the blueprints
"""
from flask import Flask
from toudou import config


def create_app():
    """
        Create the Flask app instance
        - Args :
            - None
        - Returns :
            - (Flask) : the Flask app instance
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config['SECRET_KEY']
    from toudou.web_views.routes import web_ui
    from toudou.api.routes import api, spec
    spec.register(app)
    app.register_blueprint(web_ui)
    app.register_blueprint(api)
    return app