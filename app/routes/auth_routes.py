from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies
)

auth_bp = Blueprint("auth", __name__)

# ------------------- REGISTER -------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# ------------------- LOGIN -------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    
    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

# ------------------- LOGOUT -------------------
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response, 200

# ------------------- GET USER (READ) -------------------
@auth_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })

# ------------------- UPDATE USER -------------------
@auth_bp.route("/user/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    
    if "password" in data:
        user.set_password(data["password"])
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# ------------------- DELETE USER -------------------
@auth_bp.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
