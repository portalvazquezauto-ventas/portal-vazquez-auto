# Portal Vázquez Auto

Portal web interno para el equipo comercial de Vázquez Auto.

**Stack:** Streamlit · Supabase · Anthropic API · Google Docs API

---

## Setup paso a paso

### 1. Clonar e instalar dependencias

```bash
git clone https://github.com/portalvazquezauto-ventas/portal-vazquez-auto.git
cd portal-vazquez-auto
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiá `.env.example` a `.env` y completá las claves:

```bash
cp .env.example .env
```

Variables requeridas:
- `SUPABASE_URL` — URL del proyecto Supabase
- `SUPABASE_ANON_KEY` — clave pública
- `SUPABASE_SERVICE_ROLE_KEY` — clave de servicio (para seed y admin)
- `ANTHROPIC_API_KEY` — clave de la API de Anthropic
- `GOOGLE_SERVICE_ACCOUNT_JSON` — path al JSON de service account de Google
- `GOOGLE_DOC_ID` — ID del Google Doc del manual

### 3. Configurar Supabase

En el **SQL Editor** de tu proyecto Supabase, ejecutá el script completo:

```
scripts/setup_supabase.sql
```

Esto crea todas las tablas, habilita RLS y configura las policies.

### 4. Configurar Google Docs API

1. En Google Cloud Console, creá un Service Account.
2. Descargá el JSON de credenciales.
3. Guardalo en `credentials/google_service_account.json`.
4. Compartí el Google Doc con el email del Service Account (rol: Lector).

### 5. Correr el seed inicial

```bash
python data/seed.py
```

Esto crea los 7 usuarios del sistema, carga las secciones del manual y la guía de preguntas.

### 6. Correr la aplicación

```bash
streamlit run app.py
```

---

## Usuarios del sistema

| Nombre | Email | Password | Rol |
|--------|-------|----------|-----|
| Esteban Vázquez | esteban@vazquezauto.com.ar | Direccion2026! | director |
| Victor Oller | voller@vazquezauto.com.ar | Vazquez2026! | manager |
| Leonardo Lopez | llopez@vazquezauto.com.ar | Vazquez2026! | manager |
| Matias Ribotta | mribotta@vazquezauto.com.ar | Vendedor2026! | seller |
| Lucas Lucero | llucero@vazquezauto.com.ar | Vendedor2026! | seller |
| Manuel Vazquez | mvazquez@vazquezauto.com.ar | Vendedor2026! | seller |
| Raul Pozzi | rpozzi@vazquezauto.com.ar | Vendedor2026! | seller |
| Nicolas Barrionuevo | nbarrionuevo@vazquezauto.com.ar | Vendedor2026! | seller |

---

## Módulos

- **Manual interactivo** — Secciones del manual con quiz de comprensión por sección.
- **Guía de preguntas** — Preguntas y respuestas esperadas por perfil de cliente.
- **Entrenador virtual** — Roleplay con cliente IA + evaluación de la actuación.
- **Panel de administración** — Notificaciones, actividad del manual, historial de entrenamientos, scoring, gestión de usuarios.

---

## Actualizar el manual

Los encargados y el director pueden actualizar el contenido desde **Panel de Admin → Actualizar Contenido**. Esto lee el Google Doc, parsea las secciones y regenera los quizzes con IA.
