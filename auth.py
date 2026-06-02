import streamlit as st
from supabase_client import get_client, get_admin_client


def login(email: str, password: str) -> dict | None:
    """Autentica al usuario y carga su perfil en session_state."""
    try:
        client = get_client()
        response = client.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        if not user:
            return None

        profile_resp = client.table("profiles").select("*").eq("id", user.id).single().execute()
        profile = profile_resp.data

        if not profile or not profile.get("is_active"):
            client.auth.sign_out()
            return None

        st.session_state["user"] = user
        st.session_state["profile"] = profile
        st.session_state["access_token"] = response.session.access_token
        return profile
    except Exception as e:
        return None


def logout():
    try:
        get_client().auth.sign_out()
    except Exception:
        pass
    for key in ["user", "profile", "access_token"]:
        st.session_state.pop(key, None)


def get_profile() -> dict | None:
    return st.session_state.get("profile")


def get_role() -> str | None:
    profile = get_profile()
    return profile.get("role") if profile else None


def is_logged_in() -> bool:
    return "profile" in st.session_state and st.session_state["profile"] is not None


def require_login():
    if not is_logged_in():
        st.stop()


def require_role(*roles: str):
    require_login()
    if get_role() not in roles:
        st.error("No tenés permiso para acceder a esta sección.")
        st.stop()


def is_director() -> bool:
    return get_role() == "director"


def is_manager_or_above() -> bool:
    return get_role() in ("director", "manager")


def is_seller() -> bool:
    return get_role() == "seller"


def create_user(full_name: str, email: str, password: str, role: str) -> dict | None:
    """Crea un usuario en Supabase Auth + profiles. Solo admins."""
    try:
        admin = get_admin_client()
        resp = admin.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"full_name": full_name, "role": role}
        })
        user = resp.user
        if not user:
            return None
        admin.table("profiles").upsert({
            "id": str(user.id),
            "full_name": full_name,
            "email": email,
            "role": role,
            "is_active": True,
            "must_change_password": True
        }).execute()
        return {"id": str(user.id), "full_name": full_name, "email": email, "role": role}
    except Exception as e:
        st.error(f"Error al crear usuario: {e}")
        return None


def toggle_user_active(user_id: str, is_active: bool):
    try:
        get_admin_client().table("profiles").update({"is_active": is_active}).eq("id", user_id).execute()
    except Exception as e:
        st.error(f"Error: {e}")
