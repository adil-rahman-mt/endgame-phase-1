from flask import Blueprint, jsonify
from app.api.v1.duties.models import Duties
from app.api.v1.ksb.models import KSB
from app.api.v1.ksb_duties.models import KsbDuties
from peewee import JOIN
import peewee

v2_ksb_bp = Blueprint("v2_ksb", __name__, url_prefix="ksb")

@v2_ksb_bp.get('/<name>')
def get_all_duties_for_ksb(name):
    try:
        ksb = KSB.get(KSB.name == name)
        query = (Duties
        .select(Duties.name)
        .join(KsbDuties, JOIN.INNER)
        .join(KSB, JOIN.INNER)
        .where(KSB.name == name))
        return jsonify({
            'ksb_name': ksb.name,
            'linked_to': [duty.name for duty in query]
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"KSB with name = '{name}' does not exist"
        }), 400