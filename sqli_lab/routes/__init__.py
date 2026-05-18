from sqli_lab.routes.main import main_bp
from sqli_lab.routes.auth import auth_bp
from sqli_lab.routes.learn import learn_bp
from sqli_lab.routes.practice import practice_bp
from sqli_lab.routes.challenges import challenges_bp
from sqli_lab.routes.leaderboard import leaderboard_bp
from sqli_lab.routes.api import api_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(learn_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
