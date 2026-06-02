import streamlit as st
from utils.notifications import get_unread_count


def render_notification_bell(user_id: str):
    count = get_unread_count(user_id)
    badge = f" ({count})" if count > 0 else ""
    color = "#3C3489" if count > 0 else "#6B7280"
    st.sidebar.markdown(
        f'<div style="color:{color};font-weight:{"700" if count > 0 else "400"};margin-bottom:4px">🔔 Notificaciones{badge}</div>',
        unsafe_allow_html=True
    )
    return count
