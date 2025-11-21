from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from supabase_client import supabase
from datetime import datetime, timedelta

booking_bp = Blueprint("booking", __name__)


# ---------------------- Получение списка ПК ----------------------

@booking_bp.get("/pcs")
def get_pcs():

    # получаем все ПК с характеристиками
    pcs = supabase.table("pcs").select(
        "*, cpu:cpus(name), gpu:gpus(name), os:oses(name)"
    ).execute().data

    # получаем все брони
    usages = supabase.table("pc_usages").select(
        "pc_id, start_time, end_time"
    ).eq("pc_usage_type_id", 1).execute().data

    # создаём словарь занятости
    busy_map = {}
    for u in usages:
        busy_map.setdefault(u["pc_id"], []).append({
            "start": u["start_time"],
            "end": u["end_time"]
        })

    # прикрепляем занятость к каждому ПК
    for pc in pcs:
        pc["busy"] = busy_map.get(pc["id"], [])

    return jsonify(pcs)



# ---------------------- Создание брони ----------------------

@booking_bp.post("")
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    print(data)

    pc_id = data["pc_id"]
    tariff_id = data["tariff_id"]
    start_time = datetime.fromisoformat(data["start_time"])
    duration = int(data["duration_hours"])

    # получаем тариф
    tariff = supabase.table("tariffs").select("*").eq("id", tariff_id).single().execute().data
    total_price = tariff["price_per_hour"] * duration

    # получаем пользователя
    user = supabase.table("users").select("*").eq("id", user_id).single().execute().data
    if user["balance"] < total_price:
        return jsonify({"error": "Недостаточно средств"}), 400

    end_time = start_time + timedelta(hours=duration)

    # проверка занятости ПК через RPC
    busy = supabase.rpc("check_pc_busy", {
        "pc_id": pc_id,
        "start_ts": start_time.isoformat(),
        "end_ts": end_time.isoformat()
    }).execute().data
    print(busy, pc_id, start_time.isoformat(), end_time.isoformat())

    if busy:
        return jsonify({"error": "ПК занят в это время"}), 400

    # создаём запись в pc_usages
    usage = supabase.table("pc_usages").insert({
        "pc_id": pc_id,
        "user_id": user_id,
        "pc_usage_type_id": 1,  # Активная бронь
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }).execute().data[0]

    # создаём запись в payments
    supabase.table("payments").insert({
        "tariff_id": tariff_id,
        "amount": total_price,
        "pc_usage_id": usage["id"]
    }).execute()

    # списываем деньги
    supabase.table("users").update({
        "balance": user["balance"] - total_price
    }).eq("id", user_id).execute()

    return jsonify({"message": "Бронь создана", "usage": usage})
