from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                print(f"Error verifying JWT token: {str(e)}")
                return jsonify(msg="Missing or invalid token"), 401
            
            claims = get_jwt()
            if not claims.get("is_admin"):
                return jsonify(msg="Admins only!"), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper