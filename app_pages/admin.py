import streamlit as st
import pandas as pd
from datetime import datetime
from auth import get_profile, get_role, create_user, toggle_user_active, is_director, reset_user_password
from supabase_client import get_client, get_admin_client
from components.scoring import style_score_dataframe
from utils.notifications import get_notifications, mark_all_read


def render():
    profile = get_profile()
    role = get_role()

    if role not in ("manager", "director"):
        st.error("Sin acceso.")
        return

    st.markdown("## 🏠 Panel de Administración")
    if role == "director":
        st.caption("Acceso total — Director")
    st.markdown("---")

    tabs = st.tabs(["🔔 Notificaciones", "📖 Manual", "🤖 Entrenamientos", "📊 Scoring", "👥 Usuarios", "🔄 Contenido"])

    with tabs[0]:
        _render_notifications(profile)
    with tabs[1]:
        _render_manual_activity(role)
    with tabs[2]:
        _render_training_history(role)
    with tabs[3]:
        _render_scoring(role)
    with tabs[4]:
        _render_user_management(profile, role)
    with tabs[5]:
        _render_content_update(profile)


def _render_notifications(profile):
    st.markdown("### Bandeja de notificaciones")
    notifications = get_notifications(profile["id"], limit=100)
    if not notifications:
        st.info("Sin notificaciones.")
        return

    unread = sum(1 for n in notifications if not n.get("is_read"))
    if unread:
        st.markdown(f"**{unread} sin leer**")
        if st.button("Marcar todas como leídas"):
            mark_all_read(profile["id"])
            st.rerun()

    for n in notifications:
        is_read = n.get("is_read", False)
        icon = "🔵" if not is_read else "⚪"
        type_icon = "📖" if n.get("type") == "manual_read" else "🤖"
        bg = "#FFF5F5" if not is_read else "white"
        border = "#CC1414" if not is_read else "#E5E7EB"
        st.markdown(
            f"""<div style="padding:10px;border-radius:8px;border:1px solid {border};margin-bottom:6px;background:{bg}">
            <b>{icon} {type_icon} {n['title']}</b><br>
            <span style="font-size:0.82rem;color:#555">{n.get('body','')}</span>
            <span style="float:right;font-size:0.75rem;color:#9CA3AF">{n['created_at'][:16].replace('T',' ')}</span>
            </div>""",
            unsafe_allow_html=True
        )
    mark_all_read(profile["id"])


def _render_manual_activity(role):
    st.markdown("### Actividad del manual por vendedor")
    client = get_client()
    admin_client = get_admin_client()

    # ── Reset de historial ──────────────────────────────────────
    with st.expander("🔄 Reiniciar historial de un vendedor"):
        try:
            profiles = admin_client.table("profiles").select("id,full_name").eq("role", "seller").order("full_name").execute().data or []
            if profiles:
                col1, col2 = st.columns([3, 1])
                with col1:
                    selected = st.selectbox("Vendedor", profiles, format_func=lambda x: x["full_name"], key="reset_seller")
                with col2:
                    reset_type = st.selectbox("Qué reiniciar", ["Manual", "Entrenamientos", "Todo"], key="reset_type")
                if st.button("Reiniciar historial", type="primary", key="btn_reset"):
                    if reset_type in ("Manual", "Todo"):
                        admin_client.table("manual_reads").delete().eq("user_id", selected["id"]).execute()
                    if reset_type in ("Entrenamientos", "Todo"):
                        admin_client.table("training_sessions").delete().eq("user_id", selected["id"]).execute()
                    st.success(f"✅ Historial de {selected['full_name']} reiniciado ({reset_type}).")
                    st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    try:
        reads = client.table("manual_reads").select("*, profiles(full_name), manual_sections(title, section_number)").eq("is_completed", True).order("completed_at", desc=True).execute().data or []
        if not reads:
            st.info("Sin lecturas registradas.")
            return

        rows = []
        for r in reads:
            rows.append({
                "Vendedor": r.get("profiles", {}).get("full_name", "—"),
                "Sección": f"{r.get('manual_sections', {}).get('section_number', '')}. {r.get('manual_sections', {}).get('title', '')}",
                "Fecha": r.get("completed_at", "")[:16].replace("T", " ") if r.get("completed_at") else "—",
                "Score quiz": r.get("quiz_score"),
            })
        df = pd.DataFrame(rows)
        st.dataframe(style_score_dataframe(df, ["Score quiz"]), use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


def _render_training_history(role):
    st.markdown("### Historial de entrenamientos")
    client = get_client()

    try:
        sessions = client.table("training_sessions").select("*, profiles(full_name)").eq("is_completed", True).order("completed_at", desc=True).execute().data or []
        if not sessions:
            st.info("Sin entrenamientos completados.")
            return

        sellers = sorted(set(s.get("profiles", {}).get("full_name", "—") for s in sessions))
        filter_seller = st.selectbox("Filtrar vendedor", ["Todos"] + sellers, key="ts_seller")
        filter_mode = st.selectbox("Modalidad", ["Todas", "training", "evaluation"], key="ts_mode",
                                   format_func=lambda x: {"Todas": "Todas", "training": "Entrenamiento", "evaluation": "Evaluación"}.get(x, x))

        filtered = [
            s for s in sessions
            if (filter_seller == "Todos" or s.get("profiles", {}).get("full_name") == filter_seller)
            and (filter_mode == "Todas" or s.get("mode") == filter_mode)
        ]

        rows = []
        for s in filtered:
            rows.append({
                "Vendedor": s.get("profiles", {}).get("full_name", "—"),
                "Perfil": s.get("profile_type", ""),
                "Modalidad": "Entrenamiento" if s.get("mode") == "training" else "Evaluación",
                "Indagación": s.get("score_indagacion"),
                "Objeciones": s.get("score_objeciones"),
                "Consultivo": s.get("score_consultivo"),
                "Global": s.get("score_global"),
                "Usó ayuda": "Sí" if s.get("used_hints") else "No",
                "Fecha": s.get("completed_at", "")[:16].replace("T", " ") if s.get("completed_at") else "—",
            })
        df = pd.DataFrame(rows)
        st.dataframe(style_score_dataframe(df, ["Indagación", "Objeciones", "Consultivo", "Global"]), use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


def _render_scoring(role):
    st.markdown("### Scoring general de vendedores")
    client = get_client()
    try:
        sellers = client.table("profiles").select("id, full_name").eq("role", "seller").eq("is_active", True).execute().data or []
        rows = []
        for seller in sellers:
            sid = seller["id"]
            name = seller["full_name"]

            reads = client.table("manual_reads").select("quiz_score").eq("user_id", sid).eq("is_completed", True).execute().data or []
            scores_r = [r["quiz_score"] for r in reads if r.get("quiz_score") is not None]
            avg_manual = int(sum(scores_r) / len(scores_r)) if scores_r else None

            sessions = client.table("training_sessions").select("score_global").eq("user_id", sid).eq("is_completed", True).execute().data or []
            scores_t = [s["score_global"] for s in sessions if s.get("score_global") is not None]
            avg_training = int(sum(scores_t) / len(scores_t)) if scores_t else None

            rows.append({
                "Vendedor": name,
                "Secciones completadas": len(reads),
                "Promedio quiz manual": avg_manual,
                "Sesiones entrenamiento": len(sessions),
                "Promedio entrenamiento": avg_training,
            })

        if not rows:
            st.info("Sin datos.")
            return

        df = pd.DataFrame(rows).sort_values("Promedio entrenamiento", ascending=False, na_position="last")
        df.index = range(1, len(df) + 1)
        df.index.name = "Ranking"
        st.dataframe(style_score_dataframe(df, ["Promedio quiz manual", "Promedio entrenamiento"]), use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")


def _render_user_management(profile, role):
    st.markdown("### Gestión de usuarios")

    with st.expander("➕ Crear nuevo usuario"):
        with st.form("create_user_form"):
            full_name = st.text_input("Nombre completo")
            email = st.text_input("Email")
            password = st.text_input("Contraseña inicial", type="password")
            if role == "director":
                user_role = st.selectbox("Rol", ["seller", "manager", "director"])
            else:
                user_role = "seller"
                st.caption("Los encargados solo pueden crear vendedores.")
            submitted = st.form_submit_button("Crear usuario")
            if submitted:
                if not all([full_name, email, password]):
                    st.error("Completá todos los campos.")
                else:
                    result = create_user(full_name, email, password, user_role)
                    if result:
                        st.success(f"✅ Usuario {full_name} creado correctamente.")
                        st.rerun()

    st.markdown("---")
    st.markdown("**Usuarios existentes**")
    try:
        admin = get_admin_client()
        if role == "director":
            users = admin.table("profiles").select("*").order("role").execute().data or []
        else:
            users = admin.table("profiles").select("*").eq("role", "seller").execute().data or []

        role_labels = {"director": "Director", "manager": "Encargado", "seller": "Vendedor"}
        role_colors = {"director": "#7C3AED", "manager": "#1D4ED8", "seller": "#16A34A"}

        for u in users:
            is_active = u.get("is_active", True)
            rc = role_colors.get(u["role"], "#6B7280")
            rl = role_labels.get(u["role"], u["role"])

            with st.container():
                st.markdown(
                    '<div style="background:white;border:1px solid ' + ('#E5E7EB' if is_active else '#FEE2E2') + ';'
                    'border-radius:10px;padding:12px 16px;margin-bottom:8px">'
                    '<div style="display:flex;align-items:center;gap:10px">'
                    '<div style="width:8px;height:8px;border-radius:50%;background:' + ('#16A34A' if is_active else '#DC2626') + ';flex-shrink:0"></div>'
                    '<div style="flex:1">'
                    '<span style="font-weight:700;color:#111">' + u['full_name'] + '</span> '
                    '<span style="color:#6B7280;font-size:0.82rem">' + u['email'] + '</span>'
                    '</div>'
                    '<span style="background:' + rc + '20;color:' + rc + ';padding:2px 8px;border-radius:12px;font-size:0.72rem;font-weight:700">' + rl + '</span>'
                    '</div></div>',
                    unsafe_allow_html=True
                )

                if u["id"] != profile["id"]:
                    c1, c2, c3 = st.columns([1, 1, 2])
                    with c1:
                        label = "🔒 Bloquear" if is_active else "✅ Activar"
                        if st.button(label, key=f"toggle_{u['id']}", use_container_width=True):
                            toggle_user_active(u["id"], not is_active)
                            st.rerun()
                    with c2:
                        if st.button("🔑 Nueva clave", key=f"pwdbtn_{u['id']}", use_container_width=True):
                            st.session_state[f"show_pwd_{u['id']}"] = not st.session_state.get(f"show_pwd_{u['id']}", False)
                            st.rerun()

                    if st.session_state.get(f"show_pwd_{u['id']}"):
                        with st.form(f"pwd_form_{u['id']}"):
                            new_pwd = st.text_input("Nueva contraseña", type="password", placeholder="Mínimo 8 caracteres", key=f"pwd_{u['id']}")
                            if st.form_submit_button("Guardar contraseña", type="primary"):
                                if len(new_pwd) < 8:
                                    st.error("La contraseña debe tener al menos 8 caracteres.")
                                else:
                                    if reset_user_password(u["id"], new_pwd):
                                        st.success(f"✅ Contraseña de {u['full_name']} actualizada.")
                                        st.session_state.pop(f"show_pwd_{u['id']}", None)
                                        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")


def _render_content_update(profile):
    st.markdown("### Actualizar contenido del manual")
    st.warning("Esto actualiza todas las secciones y regenera los quizzes desde Google Docs. No borra el historial de lecturas.")

    if st.button("🔄 Actualizar manual desde Google Docs", type="primary"):
        with st.spinner("Procesando..."):
            try:
                from utils.google_docs import fetch_manual_from_google_docs
                from utils.quiz_generator import generate_quiz_questions
                client = get_client()
                sections = fetch_manual_from_google_docs()
                for s in sections:
                    questions = generate_quiz_questions(s["title"], s["content"])
                    now = datetime.utcnow().isoformat()
                    existing = client.table("manual_sections").select("id").eq("section_number", s["section_number"]).execute().data
                    if existing:
                        client.table("manual_sections").update({
                            "title": s["title"],
                            "content": s["content"],
                            "quiz_questions": questions,
                            "last_updated": now,
                            "updated_by": profile["id"]
                        }).eq("id", existing[0]["id"]).execute()
                    else:
                        client.table("manual_sections").insert({
                            "section_number": s["section_number"],
                            "title": s["title"],
                            "content": s["content"],
                            "quiz_questions": questions,
                            "updated_by": profile["id"]
                        }).execute()
                st.success(f"✅ {len(sections)} secciones actualizadas.")
            except Exception as e:
                st.error(f"Error: {e}")
