import streamlit as st
from auth import get_profile
from utils.notifications import get_notifications, mark_all_read


def render():
    profile = get_profile()
    user_id = profile["id"]

    st.markdown("""
    <div style="margin-bottom:24px">
      <h2 style="margin:0;font-weight:800">🔔 Notificaciones</h2>
      <div style="height:3px;width:48px;background:#CC1414;border-radius:2px;margin-top:10px"></div>
    </div>""", unsafe_allow_html=True)

    notifications = get_notifications(user_id)
    unread = [n for n in notifications if not n.get("is_read")]

    if unread:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""<span style="background:#FEE2E2;color:#CC1414;padding:4px 12px;border-radius:20px;font-weight:700;font-size:0.82rem">{len(unread)} sin leer</span>""", unsafe_allow_html=True)
        with col2:
            if st.button("✅ Marcar todas leídas", type="primary"):
                mark_all_read(user_id)
                st.rerun()

    if not notifications:
        st.info("No tenés notificaciones todavía.")
        return

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for n in notifications:
        is_read = n.get("is_read", False)
        n_type = n.get("type", "")
        type_icon = "📖" if n_type == "manual_read" else "🤖"
        border = "#CC1414" if not is_read else "#E5E7EB"
        bg = "#FFF5F5" if not is_read else "white"
        fw = "700" if not is_read else "500"
        dot = f"""<span style="width:8px;height:8px;background:#CC1414;border-radius:50%;display:inline-block;margin-right:8px;vertical-align:middle"></span>""" if not is_read else ""

        st.markdown(
            f"""<div style="padding:14px 18px;border-radius:10px;border:1.5px solid {border};
                           margin-bottom:8px;background:{bg};box-shadow:0 1px 3px rgba(0,0,0,0.04)">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <span style="font-weight:{fw};color:#111;font-size:0.9rem">{dot}{type_icon} {n['title']}</span>
                <span style="font-size:0.72rem;color:#9CA3AF;white-space:nowrap;margin-left:12px">{n['created_at'][:16].replace('T',' ')}</span>
              </div>
              <div style="color:#6B7280;font-size:0.82rem;margin-top:6px;padding-left:16px">{n.get('body','')}</div>
            </div>""",
            unsafe_allow_html=True
        )

    mark_all_read(user_id)
