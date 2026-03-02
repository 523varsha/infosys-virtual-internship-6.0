from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_routes = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=hashed_password,
        role=data.get("role", "citizen"),
        location=data.get("location")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()

    if user and bcrypt.check_password_hash(user.password, data.get("password", "")):
        token = create_access_token(identity=str(user.id))
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "location": user.location
            }
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

@auth_routes.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "location": user.location
    }), 200
