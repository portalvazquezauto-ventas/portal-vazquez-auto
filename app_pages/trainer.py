import streamlit as st
import json
from datetime import datetime
from auth import get_profile
from supabase_client import get_client
from utils.ai_trainer import (
    PROFILES, get_opening_message, chat_with_client,
    evaluate_seller_message, get_suggested_answer,
    generate_final_feedback, calculate_global_score
)
from utils.notifications import notify_training_completed
from components.scoring import render_score_cards, render_progress_bar
import streamlit.components.v1 as components


def render():
    profile = get_profile()

    st.markdown("## 🤖 Entrenador Virtual de Ventas")
    st.markdown("Practicá una situación de venta con un cliente simulado por IA.")
    st.markdown("---")

    session_key = "trainer_session"
    if session_key not in st.session_state:
        _render_setup(profile)
    else:
        session = st.session_state[session_key]
        if session.get("is_completed"):
            _render_results(session, profile)
        else:
            _render_chat(session, profile)


def _render_setup(profile):
    st.markdown("### Configurá tu sesión")

    col1, col2 = st.columns(2)
    with col1:
        profile_type = st.selectbox(
            "Perfil de cliente",
            list(PROFILES.keys()),
            format_func=lambda x: PROFILES[x]["name"]
        )
        st.caption(PROFILES[profile_type]["description"])

    with col2:
        mode = st.radio(
            "Modalidad",
            ["training", "evaluation"],
            format_func=lambda x: "🎓 Entrenamiento (con ayuda)" if x == "training" else "📝 Evaluación (sin ayuda)"
        )
        if mode == "training":
            st.info("Podés ver respuestas sugeridas del manual en cada turno.")
        else:
            st.warning("Sin ayuda. Tu score real se registrará al terminar.")

    st.markdown("---")
    if st.button("▶️ Iniciar sesión", use_container_width=True, type="primary"):
        opening = get_opening_message(profile_type)
        st.session_state["trainer_session"] = {
            "profile_type": profile_type,
            "mode": mode,
            "messages": [{"role": "assistant", "content": opening}],
            "scores": [],
            "used_hints": False,
            "is_completed": False,
            "turn": 0,
        }
        st.rerun()


def _render_chat(session: dict, profile: dict):
    profile_info = PROFILES[session["profile_type"]]
    mode = session["mode"]

    st.markdown(f"**Perfil:** {profile_info['name']} &nbsp;|&nbsp; **Modalidad:** {'Entrenamiento' if mode == 'training' else 'Evaluación'} &nbsp;|&nbsp; **Turno:** {session['turn'] + 1}")

    _render_messages(session["messages"])

    st.markdown("---")
    st.markdown("**Tu respuesta:**")

    with open("components/voice_chat.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    voice_result = components.html(html_content, height=220, scrolling=False)

    text_input = st.text_area("O escribí acá:", key=f"text_input_{session['turn']}", label_visibility="collapsed", placeholder="Escribí tu respuesta...")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        send_clicked = st.button("📨 Enviar respuesta", use_container_width=True, type="primary", disabled=not text_input.strip())

    with col2:
        if mode == "training":
            hint_clicked = st.button("💡 Ver respuesta sugerida", use_container_width=True)
            if hint_clicked:
                last_client_msg = _get_last_client_message(session["messages"])
                suggestion = get_suggested_answer(last_client_msg, session["profile_type"])
                st.info(f"**Respuesta sugerida:** {suggestion}")
                session["used_hints"] = True

    with col3:
        end_clicked = st.button("🏁 Finalizar", use_container_width=True)

    if send_clicked and text_input.strip():
        _process_seller_turn(text_input.strip(), session, profile)
        st.rerun()

    if end_clicked and len(session["messages"]) > 1:
        _finalize_session(session, profile)
        st.rerun()


def _render_messages(messages: list):
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        feedback = msg.get("feedback")
        scores = msg.get("scores")

        if role == "assistant":
            with st.chat_message("user", avatar="🧑"):
                st.markdown(f"**Cliente:** {content}")
        else:
            with st.chat_message("assistant", avatar="💼"):
                st.markdown(f"**Vos:** {content}")
                if feedback:
                    with st.expander("📊 Feedback de este turno"):
                        st.caption(feedback)
                        if scores:
                            cols = st.columns(3)
                            with cols[0]:
                                render_progress_bar(scores.get("indagacion", 0), "Indagación")
                            with cols[1]:
                                render_progress_bar(scores.get("objeciones", 0), "Objeciones")
                            with cols[2]:
                                render_progress_bar(scores.get("consultivo", 0), "Consultivo")


def _process_seller_turn(seller_text: str, session: dict, profile: dict):
    last_client = _get_last_client_message(session["messages"])

    evaluation = evaluate_seller_message(seller_text, last_client, session["profile_type"])
    session["scores"].append(evaluation)

    session["messages"].append({
        "role": "user",
        "content": seller_text,
        "feedback": evaluation.get("feedback"),
        "scores": {k: evaluation.get(k) for k in ["indagacion", "objeciones", "consultivo"]}
    })

    client_response = chat_with_client(
        session["profile_type"],
        [{"role": m["role"], "content": m["content"]} for m in session["messages"]],
        seller_text
    )
    session["messages"].append({"role": "assistant", "content": client_response})
    session["turn"] += 1


def _finalize_session(session: dict, profile: dict):
    avg_scores = calculate_global_score(session["scores"])
    session.update(avg_scores)
    session["feedback_final"] = generate_final_feedback({
        "profile_type": session["profile_type"],
        "mode": session["mode"],
        "score_indagacion": avg_scores["indagacion"],
        "score_objeciones": avg_scores["objeciones"],
        "score_consultivo": avg_scores["consultivo"],
        "score_global": avg_scores["global"],
        "used_hints": session["used_hints"],
    })
    session["is_completed"] = True
    session["completed_at"] = datetime.utcnow().isoformat()

    _save_session(session, profile)


def _save_session(session: dict, profile: dict):
    client = get_client()
    try:
        result = client.table("training_sessions").insert({
            "user_id": profile["id"],
            "profile_type": session["profile_type"],
            "mode": session["mode"],
            "messages": session["messages"],
            "score_indagacion": session.get("indagacion"),
            "score_objeciones": session.get("objeciones"),
            "score_consultivo": session.get("consultivo"),
            "score_global": session.get("global"),
            "feedback_final": session.get("feedback_final"),
            "used_hints": session.get("used_hints", False),
            "completed_at": session.get("completed_at"),
            "is_completed": True,
        }).execute()

        session_id = result.data[0]["id"] if result.data else "unknown"

        notify_training_completed(
            user_id=profile["id"],
            user_name=profile["full_name"],
            profile_type=session["profile_type"],
            mode=session["mode"],
            score_global=session.get("global", 0),
            session_id=session_id,
            used_hints=session.get("used_hints", False)
        )
    except Exception as e:
        st.warning(f"No se pudo guardar la sesión: {e}")


def _render_results(session: dict, profile: dict):
    st.markdown("## 🏁 Sesión completada")
    st.markdown("---")

    scores = {
        "indagacion": session.get("indagacion", 0),
        "objeciones": session.get("objeciones", 0),
        "consultivo": session.get("consultivo", 0),
        "global": session.get("global", 0),
    }
    render_score_cards(scores)

    st.markdown("---")
    st.markdown("### 📝 Feedback final")
    st.info(session.get("feedback_final", "Sesión completada."))

    if session.get("used_hints"):
        st.caption("ℹ️ Usaste respuestas sugeridas durante esta sesión. Tu score refleja tus propias respuestas.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Nueva sesión", use_container_width=True):
            del st.session_state["trainer_session"]
            st.rerun()
    with col2:
        if st.button("📊 Ver historial", use_container_width=True):
            st.session_state["page"] = "admin"
            del st.session_state["trainer_session"]
            st.rerun()


def _get_last_client_message(messages: list) -> str:
    for msg in reversed(messages):
        if msg["role"] == "assistant":
            return msg["content"]
    return ""
