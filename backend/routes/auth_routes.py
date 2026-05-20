from flask import Blueprint, request, jsonify

from database.db import db
from database.models import User
from utils.password_hash import hash_password, verify_password
from utils.jwt_handler import create_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.json

    username = data["username"]
    email = data["email"]
    password = hash_password(data["password"])

    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"})


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if verify_password(password, user.password):

        token = create_token(user.id)

        return jsonify({
            "message": "Login successful",
            "token": token
        })

    return jsonify({"message": "Invalid password"}), 401