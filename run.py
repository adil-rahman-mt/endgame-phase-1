from app import create_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import limits.storage
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import jsonify, request
from flask_jwt_extended import create_access_token, JWTManager
from flask_bcrypt import Bcrypt
from app.models.users import Users
import peewee
import uuid

load_dotenv()

options = {}
redis_storage = limits.storage.storage_from_string(os.environ.get('REDIS_STORAGE_URI'), **options)

app = create_app()
bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_JWT_SECRET_KEY")
jwt = JWTManager(app)

CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per 1 minute"],
    storage_uri=os.environ.get('REDIS_STORAGE_URI'),
    strategy="fixed-window",
)

if __name__ == "__main__":
    app.run(debug=False)

@app.route('/')
def home():
    return """
    <p>Welcome to Endgame: Phase 1.</p>
    <p>For the API documentation, click <a href="https://github.com/adil-rahman-mt/endgame-phase-1">here</a></p>
    <p>Or visit https://github.com/adil-rahman-mt/endgame-phase-1</p>
    """

@app.route("/login", methods=["POST"])
@limiter.limit("6 per minute")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = Users.get_or_none(Users.username == username)

    if not username or not password:
        return jsonify({"msg": "Username and password must be provided"}), 401
    
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Login Failed'}), 401

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json() or {}
    username = data.get('username').strip().lower()
    password = data.get('password')
    is_admin = data.get('is_admin')

    if not username or not password or is_admin is None:
        return jsonify({"msg": "Enter all required fields."}), 400

    try:
        if Users.select().where(Users.username == username).exists():
            return jsonify({"msg": "A user with this username already exists."}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = Users.create(
            id=uuid.uuid4(),
            username=username,
            password=hashed_password,
            is_admin=is_admin
        )

        return jsonify({
            "msg": "User registered successfully.",
            "user": {
                "username": new_user.username
            }
        }), 201

    except peewee.DatabaseError as e:
        return jsonify({
                "msg": "Internal database error",
                "error": e
            }), 500