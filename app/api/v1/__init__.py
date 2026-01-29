from flask import Blueprint
from app.api.v1.coins.routes import coins_bp
from app.api.v1.duties.routes import duties_bp
from app.api.v1.ksb.routes import ksb_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api_v1_bp.register_blueprint(coins_bp)
api_v1_bp.register_blueprint(duties_bp)
api_v1_bp.register_blueprint(ksb_bp)