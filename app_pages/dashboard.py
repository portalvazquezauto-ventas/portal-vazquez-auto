import streamlit as st
from auth import get_profile, get_role, is_manager_or_above
from supabase_client import get_client


def _stat_card(label: str, value: str, icon: str, accent: str = "#CC1414"):
    st.markdown(f"""
    <div style="background:white;border:1.5px solid #E5E7EB;border-radius:12px;
                padding:20px 22px;box-shadow:0 1px 4px rgba(0,0,0,0.05);
                border-top:3px solid {accent}">
      <div style="color:#6B7280;font-size:0.72rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">{icon} {label}</div>
      <div style="color:#111111;font-size:1.8rem;font-weight:800;line-height:1">{value}</div>
    </div>""", unsafe_allow_html=True)


def _quick_btn(page_id: str, icon: str, label: str, desc: str):
    col_inner = st.container()
    with col_inner:
        st.markdown(f"""
        <div style="background:white;border:1.5px solid #E5E7EB;border-radius:12px;
                    padding:18px 20px;margin-bottom:4px;box-shadow:0 1px 3px rgba(0,0,0,0.04)">
          <div style="font-size:1.4rem;margin-bottom:6px">{icon}</div>
          <div style="font-weight:700;color:#111;font-size:0.95rem">{label}</div>
          <div style="color:#9CA3AF;font-size:0.78rem;margin-top:2px">{desc}</div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Abrir →", key=f"dash_{page_id}", use_container_width=True, type="primary"):
            st.session_state["page"] = page_id
            st.rerun()


def render():
    profile = get_profile()
    name = profile.get("full_name", "").split()[0]
    role = get_role()

    st.markdown(f"""
    <div style="background:white;border-radius:16px;padding:28px 32px;
                border:1.5px solid #E5E7EB;margin-bottom:28px;
                box-shadow:0 1px 6px rgba(0,0,0,0.05)">
      <div style="font-size:0.78rem;color:#CC1414;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px">Portal Comercial</div>
      <h1 style="margin:0;font-size:1.9rem;font-weight:900;color:#111">Hola, {name} 👋</h1>
      <p style="color:#6B7280;margin:6px 0 0;font-size:0.92rem">Bienvenido al portal de ventas de Vázquez Auto</p>
    </div>""", unsafe_allow_html=True)

    if role == "seller":
        _render_seller_dashboard(profile)
    else:
        _render_admin_dashboard(profile)


def _render_seller_dashboard(profile: dict):
    user_id = profile["id"]
    client = get_client()

    try:
        reads = client.table("manual_reads").select("*").eq("user_id", user_id).execute().data or []
        completed_reads = [r for r in reads if r.get("is_completed")]
        total_sections = client.table("manual_sections").select("id", count="exact").execute().count or 1

        scores = [r["quiz_score"] for r in completed_reads if r.get("quiz_score") is not None]
        avg_quiz = int(sum(scores) / len(scores)) if scores else 0

        sessions = client.table("training_sessions").select("score_global").eq("user_id", user_id).eq("is_completed", True).execute().data or []
        global_scores = [s["score_global"] for s in sessions if s.get("score_global") is not None]
        avg_training = int(sum(global_scores) / len(global_scores)) if global_scores else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            _stat_card("Manual", f"{len(completed_reads)}/{total_sections}", "📖", "#CC1414")
        with col2:
            _stat_card("Promedio quiz", f"{avg_quiz}%", "✏️", "#D97706")
        with col3:
            _stat_card("Score entrenamiento", f"{avg_training}/100", "🤖", "#16A34A")

    except Exception:
        pass

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="color:#6B7280;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px">ACCESOS RÁPIDOS</div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        _quick_btn("manual", "📖", "Manual de Ventas", "Leé y completá el quiz de cada sección")
    with col2:
        _quick_btn("guide", "🗂️", "Guía de Preguntas", "Consultá por perfil de cliente")
    with col3:
        _quick_btn("trainer", "🤖", "Entrenador Virtual", "Practicá con clientes simulados por IA")


def _render_admin_dashboard(profile: dict):
    client = get_client()

    try:
        sellers = client.table("profiles").select("id", count="exact").eq("role", "seller").eq("is_active", True).execute()
        reads = client.table("manual_reads").select("id", count="exact").eq("is_completed", True).execute()
        sessions = client.table("training_sessions").select("id", count="exact").eq("is_completed", True).execute()
        from utils.notifications import get_unread_count
        unread = get_unread_count(profile["id"])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            _stat_card("Vendedores activos", str(sellers.count or 0), "👥", "#CC1414")
        with col2:
            _stat_card("Lecturas del manual", str(reads.count or 0), "📖", "#D97706")
        with col3:
            _stat_card("Entrenamientos", str(sessions.count or 0), "🤖", "#16A34A")
        with col4:
            _stat_card("Notificaciones", str(unread), "🔔", "#CC1414")
    except Exception:
        pass

    # Progreso propio del director
    try:
        uid = profile["id"]
        my_reads = client.table("manual_reads").select("quiz_score").eq("user_id", uid).eq("is_completed", True).execute().data or []
        my_sessions = client.table("training_sessions").select("score_global").eq("user_id", uid).eq("is_completed", True).execute().data or []
        total_sections = client.table("manual_sections").select("id", count="exact").execute().count or 1
        if my_reads or my_sessions:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown("""<div style="color:#6B7280;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px">TU ACTIVIDAD</div>""", unsafe_allow_html=True)
            scores_r = [r["quiz_score"] for r in my_reads if r.get("quiz_score") is not None]
            scores_t = [s["score_global"] for s in my_sessions if s.get("score_global") is not None]
            c1, c2, c3 = st.columns(3)
            with c1:
                _stat_card("Manual", f"{len(my_reads)}/{total_sections}", "📖", "#CC1414")
            with c2:
                _stat_card("Promedio quiz", f"{int(sum(scores_r)/len(scores_r)) if scores_r else 0}%", "✏️", "#D97706")
            with c3:
                _stat_card("Score entrenamiento", f"{int(sum(scores_t)/len(scores_t)) if scores_t else 0}/100", "🤖", "#16A34A")
    except Exception:
        pass

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="color:#6B7280;font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px">ACCESOS RÁPIDOS</div>""", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _quick_btn("manual", "📖", "Manual de Ventas", "Leé y completá los quizzes")
    with col2:
        _quick_btn("guide", "🗂️", "Guía de Preguntas", "Consultá por perfil de cliente")
    with col3:
        _quick_btn("trainer", "🤖", "Entrenador Virtual", "Practicá con clientes simulados por IA")
    with col4:
        _quick_btn("admin", "⚙️", "Panel de Admin", "Gestión del equipo y contenido")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
