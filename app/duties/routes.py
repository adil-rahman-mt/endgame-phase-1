from flask import Blueprint, jsonify, request
from app.duties.models import Duties
from app.ksb.models import KSB
from app.ksb_duties.models import KsbDuties
from peewee import JOIN
import uuid 
import peewee

duties_bp = Blueprint("duties", __name__)

# DUTIES

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
        }), 404
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
        }), 409

@duties_bp.delete('/<id>')
def delete_a_duty(id):
    try:
        duty_to_delete = Duties.get_by_id(id)
        duty_to_delete.delete_instance()
        return jsonify({
            'status': "Success",
            'deleted': {
                'id': duty_to_delete.id,
                'name': duty_to_delete.name,
                'description': duty_to_delete.description,
            },
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Duty with ID = {id} does not exist"
        }), 404
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
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

# DUTY AND KSB RELATIONSHIPS

@duties_bp.get('/<duty_id>/ksb')
def get_all_ksb_for_duty(duty_id):
    try:
        query = (KSB
            .select(KSB.name)
            .join(KsbDuties, JOIN.INNER)
            .where(KsbDuties.duty_id == duty_id))
        return jsonify({
                'Duty': Duties.get_by_id(duty_id).name,
                'linked_to': [ksb.name for ksb in query]
            }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A duty with ID = {duty_id} does not exist"
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided duty ID must be a valid UUID"
        }), 400

@duties_bp.post('/<duty_id>/ksb/<ksb_id>')
def add_ksb_to_duty(duty_id, ksb_id):
    try:
        duty = Duties.get_by_id(duty_id)
        ksb = KSB.get_by_id(ksb_id)
        record = KsbDuties.create(
                id=uuid.uuid4(),
                duty_id = duty_id,
                ksb_id = ksb_id,
            )
        return jsonify({
            'id': record.id,
            'duty_id': record.duty_id.id,
            'ksb_id': record.ksb_id.id,
        }), 201
    except peewee.IntegrityError as err:
        if "already exists" in err.args[0]:
            return jsonify({
                'error': "Duplication error",
                'message': f"{ksb.name} is already associated with {duty.name}"
            }), 409
    except peewee.DoesNotExist as err:
        if "Model: Duties" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A duty with ID = {duty_id} does not exist"
            }), 404
        if "Model: KSB" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A KSB with ID = {ksb_id} does not exist"
            }), 404
        return jsonify({
                'error': "Unknown error",
            }), 400
    except peewee.DataError as err:
        return jsonify({
            'error': "Invalid ID format",
            'message': "IDs must be a valid UUID"
        }), 400

@duties_bp.delete('/<duty_id>/ksb/<ksb_id>')
def remove_duty_from_coin(duty_id, ksb_id):
    try:
        Duties.get_by_id(duty_id)
        duty_name = Duties.get_by_id(duty_id).name
        KSB.get_by_id(ksb_id)
        ksb_name = KSB.get_by_id(ksb_id).name

        record = KsbDuties.get(KsbDuties.ksb_id == ksb_id, KsbDuties.duty_id == duty_id)
        record.delete_instance()
        return jsonify({
                'status': "Success",
                'message': f"Removed {ksb_name} from {duty_name}",
            }), 200
    except peewee.DoesNotExist as err:
        if "Model: Duties" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A duty with ID = {duty_id} does not exist"
            }), 404
        if "Model: KSB" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A KSB with ID = {ksb_id} does not exist"
            }), 404
        return jsonify({
                'error': "Record does not exist",
                'message': f"{ksb_name} is not associated with {duty_name}"
            }), 404
    except peewee.DataError as err:
        return jsonify({
            'error': "Invalid ID format",
            'message': "IDs must be a valid UUID"
        }), 400