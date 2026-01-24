from flask import Flask
from app.database import db
from app.coins.routes import coins_bp
from app.duties.routes import duties_bp

def create_app():
    app = Flask(__name__)

    app.before_request
    def _db_connect():
        if db.is_closed():
            db.connect()

    app.teardown_request
    def _db_close(exc):
        if not db.is_closed():
            db.close()

    app.register_blueprint(coins_bp, url_prefix="/coins")
    app.register_blueprint(duties_bp, url_prefix="/duties")

    return app
