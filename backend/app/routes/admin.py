# backend/app/routes/admin.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from supabase_client import supabase

admin_bp = Blueprint("admin", __name__)


def is_admin():
    claims = get_jwt()
    return claims.get("role") == "Admin"


def admin_required(fn):
    def wrapper(*args, **kwargs):
        if not is_admin():
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return jwt_required()(wrapper)

# ---------------- CPU CRUD ----------------
@admin_bp.get("/cpus")
def get_cpus():
    return jsonify(supabase.table("cpus").select("*").execute().data)

@admin_bp.post("/cpus")
@admin_required
def create_cpu():
    name = request.json.get("name")
    return jsonify(supabase.table("cpus").insert({"name": name}).execute().data)

@admin_bp.put("/cpus/<int:cpu_id>")
@admin_required
def update_cpu(cpu_id):
    name = request.json.get("name")
    return jsonify(supabase.table("cpus").update({"name": name}).eq("id", cpu_id).execute().data)

@admin_bp.delete("/cpus/<int:cpu_id>")
@admin_required
def delete_cpu(cpu_id):
    return jsonify(supabase.table("cpus").delete().eq("id", cpu_id).execute().data)

# ---------------- GPU CRUD ----------------
@admin_bp.get("/gpus")
def get_gpus():
    return jsonify(supabase.table("gpus").select("*").execute().data)

@admin_bp.post("/gpus")
@admin_required
def create_gpu():
    name = request.json.get("name")
    return jsonify(supabase.table("gpus").insert({"name": name}).execute().data)

@admin_bp.put("/gpus/<int:gpu_id>")
@admin_required
def update_gpu(gpu_id):
    name = request.json.get("name")
    return jsonify(supabase.table("gpus").update({"name": name}).eq("id", gpu_id).execute().data)

@admin_bp.delete("/gpus/<int:gpu_id>")
@admin_required
def delete_gpu(gpu_id):
    return jsonify(supabase.table("gpus").delete().eq("id", gpu_id).execute().data)

# ---------------- OS CRUD ----------------
@admin_bp.get("/oses")
def get_oses():
    return jsonify(supabase.table("oses").select("*").execute().data)

@admin_bp.post("/oses")
@admin_required
def create_os():
    name = request.json.get("name")
    return jsonify(supabase.table("oses").insert({"name": name}).execute().data)

@admin_bp.put("/oses/<int:os_id>")
@admin_required
def update_os(os_id):
    name = request.json.get("name")
    return jsonify(supabase.table("oses").update({"name": name}).eq("id", os_id).execute().data)

@admin_bp.delete("/oses/<int:os_id>")
@admin_required
def delete_os(os_id):
    return jsonify(supabase.table("oses").delete().eq("id", os_id).execute().data)

# ---------------- SOFTWARE CRUD (NEW) ----------------
# Роуты для управления справочником программ

@admin_bp.get("/software")
def get_software():
    return jsonify(supabase.table("software").select("*").execute().data)

@admin_bp.post("/software")
@admin_required
def create_software():
    name = request.json.get("name")
    return jsonify(supabase.table("software").insert({"name": name}).execute().data)

@admin_bp.put("/software/<int:sw_id>")
@admin_required
def update_software(sw_id):
    name = request.json.get("name")
    return jsonify(supabase.table("software").update({"name": name}).eq("id", sw_id).execute().data)

@admin_bp.delete("/software/<int:sw_id>")
@admin_required
def delete_software(sw_id):
    # Каскадное удаление (или ошибка FK) зависит от настроек БД, 
    # но обычно сначала нужно удалить связи в pc_software.
    # Если в БД стоит ON DELETE CASCADE, то удалится само.
    # Если нет — удаляем связи вручную:
    supabase.table("pc_software").delete().eq("software_id", sw_id).execute()
    return jsonify(supabase.table("software").delete().eq("id", sw_id).execute().data)


# ---------------- Tariffs CRUD ----------------
@admin_bp.get("/tariffs")
def get_tariffs():
    return jsonify(supabase.table("tariffs").select("*").execute().data)

@admin_bp.post("/tariffs")
@admin_required
def create_tariff():
    data = request.json
    return jsonify(supabase.table("tariffs").insert(data).execute().data)

@admin_bp.put("/tariffs/<int:tid>")
@admin_required
def update_tariff(tid):
    data = request.json
    return jsonify(supabase.table("tariffs").update(data).eq("id", tid).execute().data)

@admin_bp.delete("/tariffs/<int:tid>")
@admin_required
def delete_tariff(tid):
    return jsonify(supabase.table("tariffs").delete().eq("id", tid).execute().data)

# ---------------- PC CRUD (UPDATED) ----------------

@admin_bp.get("/pcs")
@admin_required
def get_pcs():
    # Добавляем в выборку связь с pc_software и вложенную software
    # Это вернет массив pc_software: [{software: {id, name}}, ...] внутри каждого пк
    return jsonify(supabase
        .table("pcs")
        .select("*, cpu:cpus(name), gpu:gpus(name), os:oses(name), pc_software(software(*))")
        .execute()
        .data)

@admin_bp.post("/pcs")
@admin_required
def create_pc():
    data = request.json
    # Извлекаем список ID программ, если они переданы (например: [1, 5, 10])
    software_ids = data.pop("software_ids", [])
    
    # 1. Создаем ПК
    res = supabase.table("pcs").insert(data).execute()
    if not res.data:
        return jsonify({"error": "Failed to create PC"}), 400
        
    new_pc_id = res.data[0]['id']

    # 2. Если есть программы, добавляем связи в pc_software
    if software_ids:
        relations = [{"pc_id": new_pc_id, "software_id": sid} for sid in software_ids]
        supabase.table("pc_software").insert(relations).execute()

    return jsonify(res.data)

@admin_bp.put("/pcs/<int:pc_id>")
@admin_required
def update_pc(pc_id):
    data = request.json
    software_ids = data.pop("software_ids", None) # None значит поле не передали, [] значит очистить

    # 1. Обновляем основные поля ПК
    res = supabase.table("pcs").update(data).eq("id", pc_id).execute()

    # 2. Обновляем программы (только если поле software_ids было в запросе)
    if software_ids is not None:
        # Удаляем старые связи
        supabase.table("pc_software").delete().eq("pc_id", pc_id).execute()
        
        # Если список не пуст, добавляем новые
        if len(software_ids) > 0:
            relations = [{"pc_id": pc_id, "software_id": sid} for sid in software_ids]
            supabase.table("pc_software").insert(relations).execute()

    return jsonify(res.data)

@admin_bp.delete("/pcs/<int:pc_id>")
@admin_required
def delete_pc(pc_id):
    # Сначала удаляем связи с софтом
    supabase.table("pc_software").delete().eq("pc_id", pc_id).execute()
    return jsonify(supabase.table("pcs").delete().eq("id", pc_id).execute().data)