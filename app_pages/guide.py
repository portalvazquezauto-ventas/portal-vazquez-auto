import streamlit as st
from supabase_client import get_client

PROFILE_LABELS = {
    "precio": "💰 El que pelea precio",
    "indeciso": "🤔 El indeciso",
    "informado": "🔍 El sobre-informado",
    "agro": "🌾 El cliente agro",
    "credito": "💳 El que necesita crédito",
    "primera_compra": "🚗 Primera compra",
    "general": "⚡ Objeciones generales",
}

CATEGORY_LABELS = {
    "indagacion": "🔎 Indagación",
    "objecion": "🛡️ Manejo de objeciones",
    "construccion": "🏗️ Construcción de valor",
    "herramienta": "🛠️ Herramientas",
    "validacion": "✅ Validación",
    "diferencial": "⭐ Diferencial",
    "tecnica": "⚙️ Técnica",
    "servicio": "🔧 Servicio",
    "pre_evaluacion": "📋 Pre-evaluación",
    "proceso": "📝 Proceso",
    "cierre": "🤝 Cierre",
}


def render():
    client = get_client()

    col_title, col_back = st.columns([6, 1])
    with col_title:
        st.markdown("## 🗂️ Guía de Preguntas Estructurada")
        st.markdown("Consultá antes de una visita o llamada. Hacé clic en una pregunta para ver la respuesta esperada.")
    with col_back:
        st.markdown('<div style="padding-top:6px"></div>', unsafe_allow_html=True)
        if st.button("🏠 Inicio", key="guide_back_home", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    st.markdown("---")

    data = _load_guide(client)
    if not data:
        st.info("No hay contenido cargado en la guía.")
        return

    all_profiles = sorted(set(r["profile_type"] for r in data))
    all_categories = sorted(set(r["category"] for r in data))

    col1, col2 = st.columns(2)
    with col1:
        profile_filter = st.selectbox(
            "Perfil de cliente",
            ["Todos"] + all_profiles,
            format_func=lambda x: PROFILE_LABELS.get(x, x) if x != "Todos" else "Todos los perfiles"
        )
    with col2:
        cat_filter = st.selectbox(
            "Categoría",
            ["Todas"] + all_categories,
            format_func=lambda x: CATEGORY_LABELS.get(x, x) if x != "Todas" else "Todas las categorías"
        )

    filtered = [
        r for r in data
        if (profile_filter == "Todos" or r["profile_type"] == profile_filter)
        and (cat_filter == "Todas" or r["category"] == cat_filter)
    ]

    if not filtered:
        st.info("No hay preguntas para los filtros seleccionados.")
        return

    st.markdown(f"**{len(filtered)} preguntas encontradas**")
    st.markdown("---")

    current_profile = None
    for row in sorted(filtered, key=lambda x: (x["profile_type"], x["order_index"])):
        if row["profile_type"] != current_profile:
            current_profile = row["profile_type"]
            st.markdown(f"### {PROFILE_LABELS.get(current_profile, current_profile)}")

        cat_label = CATEGORY_LABELS.get(row["category"], row["category"])
        ref = f" · _Manual sección {row['manual_reference']}_" if row.get("manual_reference") else ""

        with st.expander(f"**{row['question']}** — {cat_label}{ref}"):
            st.markdown(f"**Respuesta esperada:**")
            st.markdown(f"> {row['expected_answer']}")
            if row.get("manual_reference"):
                st.caption(f"📚 Referencia: Sección {row['manual_reference']} del manual")


def _load_guide(client) -> list[dict]:
    try:
        resp = client.table("question_guide").select("*").order("order_index").execute()
        return resp.data or []
    except Exception:
        return []
