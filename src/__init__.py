from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Init db
db = SQLAlchemy()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_flask_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')

def create_app():
    # Load env variables
    load_dotenv()

    # Create app
    app = Flask(__name__)
    # Handling CORS
    CORS(app)

    app.config.from_object(Config)

    # Config section
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER"),
            DB_PASSWORD=os.getenv("DB_PASSWORD"),
            DB_HOST=os.getenv("DB_HOST"),
            DB_NAME=os.getenv("DB_NAME"),
        )
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the db to app
    db.init_app(app)

    jwt = JWTManager(app) 

    # Init migration
    migrate = Migrate(app, db)

    # Import routes
    from src.routes.auth_routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
