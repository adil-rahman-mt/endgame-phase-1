from flask import Blueprint, jsonify, request
from app.duties.models import Duties
import uuid 
import peewee

duties_bp = Blueprint("duties", __name__)

@duties_bp.get("")
def get_all_duties():
    duties = [duty for duty in Duties.select().dicts()]
    return jsonify(duties), 200

@duties_bp.get('/<id>')
def get_duty_by_id(id):
    try:
        duty = Duties.get_by_id(id)
        return jsonify({
            'id': duty.id,
            'name': duty.name,
            'description': duty.description
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Duty with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@duties_bp.post('')
def create_new_duty():
    data = request.get_json()

    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid json input'}), 400
    
    try:
        new_duty = Duties.create(
            id=uuid.uuid4(),
            name=data['name'],
            description=data['description'],
        )
        return jsonify({
        'id': new_duty.id,
        'name': new_duty.name,
        'description': new_duty.description,
    }), 201
    except peewee.IntegrityError as err:
        return jsonify({
            'error': "Duplication error",
            'message': f"A duty with {err.args[0].split(':  ')[-1][4:-17]} already exists",
        }), 400

@duties_bp.delete('/<id>')
def delete_a_duty(id):
    try:
        duty_to_delete = Duties.get(Duties.id == f"{id}")
        duty_to_delete.delete_instance()
        return jsonify({
            'status': "Success",
            'message': f"Duty with ID = {id} has been deleted",
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Duty with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@duties_bp.patch('/<id>')
def update_a_duty(id):
    try:
        data = request.get_json()
        duty = Duties.get(Duties.id == f"{id}")

        if 'name' in data:
            duty.name = data["name"]
            duty.save()
    
        if 'description' in data:
            duty.description = data["description"]
            duty.save()
        
        updated_duty = Duties.get(Duties.id == f"{id}")
        return jsonify({
            "id": updated_duty.id,
            "name": updated_duty.name,
            "description": updated_duty.description
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Duty with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400
