# backend/routes/auth.py

from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.decorators import user_required, admin_required, agent_required, referrer_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Missing required fields.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists.'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials.'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200
