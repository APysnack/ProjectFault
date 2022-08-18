from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from application.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from application.blueprints.ancillary.routes import ancillary
    from application.blueprints.api.routes import api
    from application.blueprints.artwork.routes import artwork
    from application.blueprints.audio.routes import audio
    from application.blueprints.code.routes import code
    from application.blueprints.games.routes import games
    from application.blueprints.errors.handlers import errors
    from application.blueprints.main.routes import main
    from application.blueprints.posts.routes import posts
    from application.blueprints.text.routes import text
    from application.blueprints.users.routes import users
    from application.blueprints.video.routes import video

    app.register_blueprint(ancillary)
    app.register_blueprint(api)
    app.register_blueprint(artwork)
    app.register_blueprint(audio)
    app.register_blueprint(code)
    app.register_blueprint(games)
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(text)
    app.register_blueprint(users)
    app.register_blueprint(video)

    return app
