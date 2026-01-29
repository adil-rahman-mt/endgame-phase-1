from flask import Blueprint
from app.api.v2.duties.routes import v2_duties_bp

api_v2_bp = Blueprint("api_v2", __name__, url_prefix="/api/v2")

api_v2_bp.register_blueprint(v2_duties_bp)