# backend/decorators.py

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from backend.models import User

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({"msg": "Admin privilege required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def agent_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'agent':
            return jsonify({"msg": "Agent privilege required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def referrer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'referrer':
            return jsonify({"msg": "Referrer privilege required"}), 403
        return fn(*args, **kwargs)
    return wrapper
