from flask import Blueprint, jsonify
from app.models.duties import Duties
from app.models.coins import Coins
from app.models.coin_duties import CoinDuties
from peewee import JOIN
import peewee

v2_duties_bp = Blueprint("v2_duties", __name__, url_prefix="duties")

@v2_duties_bp.get('/<name>')
def get_all_coins_for_duty(name):
    try:
        duty = Duties.get(Duties.name == name)
        query = (Coins
        .select(Coins.name)
        .join(CoinDuties, JOIN.INNER)
        .join(Duties, JOIN.INNER)
        .where(Duties.name == name))
        return jsonify({
            'duty_name': duty.name,
            'linked_to': [coin.name for coin in query]
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Duty with name = '{name}' does not exist"
        }), 400