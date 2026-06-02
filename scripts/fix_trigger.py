"""
Ejecuta el SQL de fix del trigger via Supabase Management API.
Requiere SUPABASE_ACCESS_TOKEN (token personal de supabase.com)
O usa el enfoque alternativo de sign_up para crear usuarios.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

import httpx

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# SQL para hacer el trigger más tolerante
SQL = """
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  BEGIN
    INSERT INTO profiles (id, full_name, role, email)
    VALUES (
      NEW.id,
      COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
      COALESCE(NEW.raw_user_meta_data->>'role', 'seller'),
      NEW.email
    )
    ON CONFLICT (id) DO UPDATE SET
      full_name = EXCLUDED.full_name,
      role = EXCLUDED.role,
      email = EXCLUDED.email;
  EXCEPTION WHEN OTHERS THEN
    -- Ignorar errores del trigger para no bloquear la creación del usuario
    NULL;
  END;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
"""

headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
}

# Intentar via RPC (necesita que exista una función)
print("Intentando fix via API...")

# Usar el endpoint de administración directamente
try:
    resp = httpx.post(
        f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
        headers=headers,
        json={"query": SQL},
        timeout=15
    )
    print(f"RPC status: {resp.status_code} - {resp.text[:200]}")
except Exception as e:
    print(f"RPC no disponible: {e}")

print("\nEl trigger fix debe ejecutarse manualmente en el SQL Editor de Supabase.")
print("Copiá este SQL y ejecutalo:")
print("="*60)
print(SQL)
print("="*60)
