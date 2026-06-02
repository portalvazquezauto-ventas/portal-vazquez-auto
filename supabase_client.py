import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None
_admin_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_ANON_KEY son requeridas")
        _client = create_client(url, key)
    return _client


def get_admin_client() -> Client:
    """Cliente con service_role — solo para operaciones de admin (seed, crear usuarios)."""
    global _admin_client
    if _admin_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY son requeridas")
        _admin_client = create_client(url, key)
    return _admin_client
