from flask import Blueprint, jsonify
from database.models import User

user_bp = Blueprint("users", __name__)

@user_bp.route("/users")
def get_users():

    users = User.query.all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    return jsonify(result)