import os, click

from src.models.base import db, migrate, jwt
from flask import Flask, current_app
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

bcrypt = Bcrypt()
ma = Marshmallow()

spec = APISpec(
    title="DIO BANK",
    version="1.0.0",
    openapi_version = '3.0.4',
    info=dict(description="DIO BANK API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


#Config banco
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///diobank.sqlite',
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'],
        JWT_SECRET_KEY = "super_secret"
        
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    #Import blueprint
    from src.controllers import user,auth, role
    
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    
    @app.route('/docs')
    def docs():
        return spec.path(view=user.delete_user).path(view=user.get_user).to_dict()
    
    from flask import json
    from werkzeug.exceptions import HTTPException
    
    @app.errorhandler(HTTPException)
    def handle_exeception(e):
        response = e.get_response()
        response.data = json.dumps(
        {
            "code": e.code,
            "name":e.name,
            "description": e.description,
        }
        )
        response.content_type = "application/json"
        return response
    
    
    return app