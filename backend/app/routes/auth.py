from flask import Blueprint, request, jsonify
from supabase_client import supabase
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    full_name = data["full_name"]

    # Проверка существования пользователя
    existing = supabase.table("users").select("id").eq("email", email).execute()
    if existing.data:
        return jsonify({"error": "Email уже существует"}), 400

    hashed = generate_password_hash(password)

    user = {
        "email": email,
        "full_name": full_name,
        "password_hash": hashed,
        "balance": 500,
        "role": "User",
    }

    created = supabase.table("users").insert(user).execute()

    return jsonify({"message": "Регистрация успешна"})


@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    r = supabase.table("users").select("*").eq("email", email).execute()
    if not r.data:
        return jsonify({"error": "Неверный email или пароль"}), 401

    user = r.data[0]

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Неверный email или пароль"}), 401

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({
        "access_token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "balance": user["balance"],
        }
    })


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = int(get_jwt_identity())

    r = supabase.table("users").select("*").eq("id", user_id).execute()

    if not r.data:
        return jsonify({"error": "User not found"}), 404

    user = r.data[0]

    return jsonify({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "balance": user["balance"],
        "full_name": user["full_name"]
    })