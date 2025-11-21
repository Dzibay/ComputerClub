from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from supabase_client import supabase
from datetime import datetime

cabinet_bp = Blueprint("cabinet", __name__)


@cabinet_bp.get("")
@jwt_required()
def cabinet():
    user_id = get_jwt_identity()

    user = supabase.table("users").select("id, full_name, email, balance").eq("id", user_id).execute().data[0]

    now = datetime.utcnow().isoformat()

    booking = (
        supabase.table("pc_usages")
        .select("*")
        .eq("user_id", user_id)
        .eq("pc_usage_type_id", 1)
        .gt("end_time", now)
        .execute().data
    )

    return jsonify({
        "user": user,
        "active_booking": booking[0] if booking else None
    })


@cabinet_bp.post("/cancel")
@jwt_required()
def cancel_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    booking_id = data["booking_id"]

    # Получаем бронь
    r = supabase.table("pc_usages").select("*").eq("id", booking_id).eq("user_id", user_id).execute()
    if not r.data:
        return jsonify({"error": "Бронь не найдена"}), 404

    booking = r.data[0]

    # Получаем платёж
    payment = supabase.table("payments").select("*").eq("pc_usage_id", booking_id).execute().data[0]

    # Обновляем баланс
    supabase.table("users").update({
        "balance": supabase.rpc("add_balance", {
            "uid": user_id,
            "amount": payment["amount"]
        }).execute()
    })

    # Меняем статус брони
    supabase.table("pc_usages").update({"pc_usage_type_id": 2}).eq("id", booking_id).execute()

    return jsonify({"message": "Бронь отменена"})
