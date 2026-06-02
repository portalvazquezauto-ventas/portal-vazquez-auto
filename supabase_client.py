import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None
_admin_client: Client | None = None


def _get_secret(key: str) -> str | None:
    """Lee desde st.secrets (Streamlit Cloud) o desde variables de entorno (.env local)."""
    try:
        import streamlit as st
        return st.secrets.get(key)
    except Exception:
        pass
    return os.getenv(key)


def get_client() -> Client:
    global _client
    if _client is None:
        url = _get_secret("SUPABASE_URL")
        key = _get_secret("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_ANON_KEY son requeridas")
        _client = create_client(url, key)
    return _client


def get_admin_client() -> Client:
    global _admin_client
    if _admin_client is None:
        url = _get_secret("SUPABASE_URL")
        key = _get_secret("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY son requeridas")
        _admin_client = create_client(url, key)
    return _admin_client
