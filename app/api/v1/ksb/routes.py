from flask import Blueprint, jsonify, request
from app.api.v1.ksb.models import KSB
import uuid 
import peewee

ksb_bp = Blueprint("ksbs", __name__, url_prefix="ksb")

@ksb_bp.get("")
def get_all_ksbs():
    ksbs = [ksb for ksb in KSB.select().dicts()]
    return jsonify(ksbs), 200

@ksb_bp.get('/<id>')
def get_ksb_by_id(id):
    try:
        ksb = KSB.get_by_id(id)
        return jsonify({
            'id': ksb.id,
            'type': ksb.type,
            'name': ksb.name,
            'description': ksb.description
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"KSB with ID = {id} does not exist"
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@ksb_bp.post('')
def create_new_ksb():
    data = request.get_json()

    if not data or 'type' not in data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid json input'}), 400
    
    if data['type'] not in ['Knowledge', 'Skill', 'Behaviour']:
        return jsonify({
            'error': "Invalid type",
            'message': "Type must be one of 'Knowledge', 'Skill' or 'Behaviour'",
        }), 400
    
    try:
        new_ksb = KSB.create(
            id=uuid.uuid4(),
            type=data['type'],
            name=data['name'],
            description=data['description'],
        )
        return jsonify({
            'id': new_ksb.id,
            'type': new_ksb.type,
            'name': new_ksb.name,
            'description': new_ksb.description,
        }), 201
    except peewee.IntegrityError as err:
        return jsonify({
            'error': "Duplication error",
            'message': f"A KSB with {err.args[0].split(':  ')[-1][4:-17]} already exists",
        }), 409

@ksb_bp.delete('/<id>')
def delete_a_ksb(id):
    try:
        ksb_to_delete = KSB.get_by_id(id)
        ksb_to_delete.delete_instance()
        return jsonify({
            'status': "Success",
            'deleted': {
                'id': ksb_to_delete.id,
                'type': ksb_to_delete.type,
                'name': ksb_to_delete.name,
                'description': ksb_to_delete.description,
            },
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"KSB with ID = {id} does not exist"
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@ksb_bp.patch('/<id>')
def update_a_ksb(id):
    try:
        data = request.get_json()
        ksb = KSB.get(KSB.id == f"{id}")

        if 'type' in data and data['type'] not in ['Knowledge', 'Skill', 'Behaviour']:
            return jsonify({
                'error': "Invalid type",
                'message': "Type must be one of 'Knowledge', 'Skill' or 'Behaviour'",
            }), 400

        if 'type' in data:
            ksb.type = data["type"]
            ksb.save()

        if 'name' in data:
            ksb.name = data["name"]
            ksb.save()
    
        if 'description' in data:
            ksb.description = data["description"]
            ksb.save()
        
        updated_ksb = KSB.get(KSB.id == f"{id}")
        return jsonify({
            "id": updated_ksb.id,
            "type": updated_ksb.type,
            "name": updated_ksb.name,
            "description": updated_ksb.description
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"KSB with ID = {id} does not exist"
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400
