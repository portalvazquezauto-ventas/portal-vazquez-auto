from datetime import datetime
from supabase_client import get_client, get_admin_client


def _get_all_managers_and_directors() -> list[dict]:
    try:
        resp = get_admin_client().table("profiles").select("id, role").in_("role", ["manager", "director"]).eq("is_active", True).execute()
        return resp.data or []
    except Exception:
        return []


def notify_manual_read(user_id: str, user_name: str, section_title: str, quiz_score: int, quiz_answers: dict, section_id: int):
    recipients = _get_all_managers_and_directors()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    client = get_admin_client()

    for recipient in recipients:
        if recipient["id"] == user_id:
            continue
        try:
            client.table("notifications").insert({
                "recipient_id": recipient["id"],
                "type": "manual_read",
                "sender_id": user_id,
                "title": f"Nueva visualización del manual — {user_name}",
                "body": f"Sección: {section_title} | Score quiz: {quiz_score}% | {now}",
                "payload": {
                    "user_id": user_id,
                    "section_id": section_id,
                    "quiz_score": quiz_score,
                    "quiz_answers": quiz_answers,
                    "completed_at": now
                }
            }).execute()
        except Exception:
            pass


def notify_training_completed(user_id: str, user_name: str, profile_type: str, mode: str, score_global: int, session_id: str, used_hints: bool):
    recipients = _get_all_managers_and_directors()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    mode_label = "Entrenamiento" if mode == "training" else "Evaluación"
    client = get_admin_client()

    for recipient in recipients:
        if recipient["id"] == user_id:
            continue
        try:
            client.table("notifications").insert({
                "recipient_id": recipient["id"],
                "type": "training_completed",
                "sender_id": user_id,
                "title": f"Nuevo entrenamiento — {user_name}",
                "body": f"Perfil: {profile_type} | Modalidad: {mode_label} | Score global: {score_global}/100 | {now}",
                "payload": {
                    "user_id": user_id,
                    "session_id": session_id,
                    "profile_type": profile_type,
                    "mode": mode,
                    "score_global": score_global,
                    "used_hints": used_hints,
                    "completed_at": now
                }
            }).execute()
        except Exception:
            pass


def get_unread_count(user_id: str) -> int:
    try:
        resp = get_client().table("notifications").select("id", count="exact").eq("recipient_id", user_id).eq("is_read", False).execute()
        return resp.count or 0
    except Exception:
        return 0


def mark_all_read(user_id: str):
    try:
        get_client().table("notifications").update({"is_read": True}).eq("recipient_id", user_id).eq("is_read", False).execute()
    except Exception:
        pass


def get_notifications(user_id: str, limit: int = 50) -> list[dict]:
    try:
        resp = get_client().table("notifications").select("*").eq("recipient_id", user_id).order("created_at", desc=True).limit(limit).execute()
        return resp.data or []
    except Exception:
        return []
