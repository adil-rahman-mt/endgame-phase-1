from flask import Flask
from app.database import db
from app.api.v1 import api_v1_bp

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

    app.register_blueprint(api_v1_bp)

    return app
