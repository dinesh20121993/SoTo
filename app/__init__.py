from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(config_name="default"):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import bp as auth_bp
    from .routes.dashboard import bp as dashboard_bp
    from .routes.sections import bp as sections_bp
    from .routes.goals import bp as goals_bp
    from .routes.shopping import bp as shopping_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(sections_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(shopping_bp)

    with app.app_context():
        db.create_all()

    return app
