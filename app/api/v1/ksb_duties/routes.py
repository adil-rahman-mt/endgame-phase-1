from flask import Blueprint, jsonify, request
from app.api.v1.ksb_duties.models import KsbDuties
import uuid 
import peewee

ksb_duties_bp = Blueprint("ksb_duties", __name__, url_prefix="/ksb-duties")

@ksb_duties_bp.get("")
def get_all():
    ksb_duties = [ksb_duty for ksb_duty in KsbDuties.select().dicts()]
    return jsonify(ksb_duties), 200

@ksb_duties_bp.get('/<id>')
def get_by_id(id):
    try:
        record = KsbDuties.get_by_id(id)
        return jsonify({
            'id': record.id,
            'ksb_id': record.ksb_id.id,
            'duty_id': record.duty_id.id,
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A record with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@ksb_duties_bp.post('')
def create():
    data = request.get_json()

    if not data or 'ksb_id' not in data or 'duty_id' not in data:
        return jsonify({'error': 'Invalid json input'}), 400
    
    try:
        record = KsbDuties.create(
            id=uuid.uuid4(),
            ksb_id=data['ksb_id'],
            duty_id=data['duty_id']
        )
        return jsonify({
            'id': record.id,
            'ksb_id': record.ksb_id.id,
            'duty_id': record.duty_id.id,
        }), 201
    except peewee.IntegrityError as err:
        if "already exists" in err.args[0]:
            return jsonify({
                'error': "Duplication error",
                'message': "This record already exists"
            }), 400
        if "not present in table" in err.args[0]:
            return jsonify({
                'error': "Input error",
                'message': f"{err.args[0].split('DETAIL:')[-1][2:-1]}"
            }), 400
        return jsonify({
                'error': "Unknown error",
            }), 400
    except peewee.DataError as err:
        return jsonify({
            'error': "Invalid ID format",
            'message': "IDs must be a valid UUID"
        }), 400

@ksb_duties_bp.delete('/<id>')
def delete(id):
    try:
        record = KsbDuties.get_by_id(id)
        record.delete_instance()
        return jsonify({
            'status': "Success",
            'deleted': {
                'id': record.id,
                'ksb_id': record.ksb_id.id,
                'duty_id': record.duty_id.id
            },
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A record with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@ksb_duties_bp.patch('/<id>')
def update(id):
    try:
        data = request.get_json()
        record = KsbDuties.get_by_id(id)

        if 'ksb_id' in data:
            record.ksb_id = data["ksb_id"]
        if 'duty_id' in data:
            record.duty_id = data["duty_id"]
        
        record.save()
        updated_record = KsbDuties.get_by_id(id)

        return jsonify({
            "id": updated_record.id,
            "ksb_id": updated_record.ksb_id.id,
            "duty_id": updated_record.duty_id.id
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A record with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400
