import streamlit as st
from dotenv import load_dotenv
import base64, os

load_dotenv()

st.set_page_config(
    page_title="Portal Vázquez Auto",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Paleta Vázquez Auto ──────────────────────────────────────
# Rojo principal: #CC1414  |  Blanco: #FFFFFF  |  Negro: #111111
# Gris oscuro: #1A1A1A  |  Gris medio: #6B7280  |  Gris claro: #F4F4F4
# Verde éxito: #16A34A  |  Ámbar: #D97706  |  Rojo error: #DC2626

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
  }

  /* ── Variables ── */
  :root {
    --red: #CC1414;
    --red-dark: #A50E0E;
    --red-light: #FEE2E2;
    --black: #111111;
    --gray-dark: #374151;
    --gray-mid: #6B7280;
    --gray-light: #F4F4F4;
    --white: #FFFFFF;
    --green: #16A34A;
    --amber: #D97706;
    --border: #E5E7EB;
  }

  /* ── Fondo general ── */
  .stApp { background: #F9F9F9; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: none !important;
  }
  section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
  }
  section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid #333333 !important;
    color: #CCCCCC !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    background: #1F1F1F !important;
    border-color: #CC1414 !important;
    color: #FFFFFF !important;
  }
  section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #CC1414 !important;
    border-color: #CC1414 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
  }

  /* ── Botones principales ── */
  .stButton > button[kind="primary"] {
    background: #CC1414 !important;
    border-color: #CC1414 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    letter-spacing: 0.01em !important;
    transition: background 0.15s ease !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: #A50E0E !important;
    border-color: #A50E0E !important;
  }
  .stButton > button[kind="secondary"] {
    border-radius: 8px !important;
    font-weight: 500 !important;
  }

  /* ── Headings ── */
  h1, h2, h3 { color: #111111 !important; font-weight: 800 !important; letter-spacing: -0.02em; }
  h1 { font-size: 2rem !important; }
  h2 { font-size: 1.5rem !important; }
  h3 { font-size: 1.15rem !important; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 2px solid #E5E7EB; }
  .stTabs [data-baseweb="tab"] {
    border-radius: 6px 6px 0 0 !important;
    font-weight: 600 !important;
    color: #6B7280 !important;
    padding: 8px 16px !important;
  }
  .stTabs [aria-selected="true"] {
    background: #CC1414 !important;
    color: #FFFFFF !important;
    border-bottom: 2px solid #CC1414 !important;
  }

  /* ── Cards / containers ── */
  .vazquez-card {
    background: white;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }

  /* ── Métricas ── */
  [data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  [data-testid="stMetricLabel"] { color: #6B7280 !important; font-size: 0.8rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em; }
  [data-testid="stMetricValue"] { color: #111111 !important; font-weight: 800 !important; }

  /* ── Progress ── */
  .stProgress > div > div { background: #CC1414 !important; border-radius: 4px; }

  /* ── Forms / inputs ── */
  .stTextInput input, .stTextArea textarea, .stSelectbox select {
    border-radius: 8px !important;
    border: 1.5px solid #E5E7EB !important;
    font-family: 'Inter', sans-serif !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #CC1414 !important;
    box-shadow: 0 0 0 3px rgba(204,20,20,0.1) !important;
  }

  /* ── Alerts ── */
  .stSuccess { background: #F0FDF4 !important; border-left: 4px solid #16A34A !important; border-radius: 8px !important; }
  .stWarning { background: #FFFBEB !important; border-left: 4px solid #D97706 !important; border-radius: 8px !important; }
  .stError   { background: #FEF2F2 !important; border-left: 4px solid #DC2626 !important; border-radius: 8px !important; }
  .stInfo    { background: #FEF2F2 !important; border-left: 4px solid #CC1414 !important; border-radius: 8px !important; }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    font-weight: 600 !important;
    border-radius: 8px !important;
    background: #F9F9F9 !important;
  }

  /* ── Divisores ── */
  hr { border: none; border-top: 1.5px solid #E5E7EB; margin: 20px 0; }

  /* ── Ocultar elementos de Streamlit ── */
  [data-testid="stSidebarNav"] { display: none !important; }
  [data-testid="stToolbar"] { display: none !important; }
  #MainMenu { display: none !important; }
  footer { display: none !important; }
  header[data-testid="stHeader"] { background: transparent !important; }
  /* Ocultar botón Deploy */
  .stDeployButton { display: none !important; }
  button[kind="header"] { display: none !important; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #CC1414; }

  /* ── Chat messages ── */
  [data-testid="stChatMessage"] {
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
    margin-bottom: 8px !important;
  }

  /* ── Dataframe ── */
  .stDataFrame { border-radius: 10px !important; overflow: hidden; }

  /* ── Radio buttons ── */
  .stRadio label { font-weight: 500; }

  /* ── Caption ── */
  .stCaption { color: #9CA3AF !important; font-size: 0.78rem !important; }

  /* ── Badge rojo header ── */
  .vz-header-bar {
    background: #CC1414;
    color: white;
    padding: 8px 20px;
    margin: -1rem -1rem 1.5rem -1rem;
    border-radius: 0 0 12px 12px;
    font-weight: 700;
    letter-spacing: 0.02em;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 10px;
  }
</style>
""", unsafe_allow_html=True)


def _logo_html(size: str = "normal") -> str:
    if size == "small":
        return """
        <div style="display:flex;align-items:center;gap:8px;padding:16px 0 12px">
          <div style="background:#CC1414;color:white;font-weight:900;font-size:1.1rem;
                      padding:4px 10px;border-radius:4px;letter-spacing:0.04em;line-height:1.2">
            V<span style="font-size:0.7em;font-weight:400">ÁZQUEZ</span>
          </div>
          <div style="color:#CCCCCC;font-size:0.7rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;line-height:1.1">
            AUTO<br><span style="opacity:0.5;font-size:0.65rem">Portal Comercial</span>
          </div>
        </div>"""
    return """
    <div style="text-align:center;padding:48px 0 32px">
      <div style="display:inline-flex;align-items:center;gap:12px;margin-bottom:12px">
        <div style="background:#CC1414;color:white;font-weight:900;font-size:2.2rem;
                    padding:8px 18px;border-radius:6px;letter-spacing:0.03em;line-height:1.1">
          V<span style="font-size:0.65em;font-weight:400">ÁZQUEZ</span>
        </div>
        <div style="font-size:1rem;font-weight:800;letter-spacing:0.2em;color:#111;text-transform:uppercase;line-height:1.1">
          AUTO
        </div>
      </div>
      <div style="color:#6B7280;font-size:0.9rem;margin-top:4px">Portal interno del equipo comercial</div>
    </div>"""


def render_login():
    # Ocultar sidebar en login
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    .block-container { max-width: 480px !important; padding-top: 4rem !important; }
    </style>""", unsafe_allow_html=True)

    st.markdown(_logo_html("normal"), unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="tu@vazquezauto.com.ar")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")
        submit = st.form_submit_button("Ingresar →", use_container_width=True, type="primary")

        if submit:
            if not email or not password:
                st.error("Completá email y contraseña.")
            else:
                from auth import login
                with st.spinner(""):
                    profile = login(email, password)
                if profile:
                    st.session_state["page"] = "dashboard"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas o usuario inactivo.")

    st.markdown("""
    <div style="text-align:center;margin-top:24px;color:#9CA3AF;font-size:0.75rem">
      © 2026 Vázquez Auto · Uso interno
    </div>""", unsafe_allow_html=True)


def render_sidebar(profile: dict, role: str):
    with st.sidebar:
        st.markdown(_logo_html("small"), unsafe_allow_html=True)

        role_labels = {"director": "Director", "manager": "Encargado", "seller": "Vendedor"}
        role_colors = {"director": "#CC1414", "manager": "#F59E0B", "seller": "#6B7280"}
        rc = role_colors.get(role, "#6B7280")

        st.markdown(f"""
        <div style="background:#1F1F1F;border-radius:10px;padding:12px 14px;margin-bottom:16px">
          <div style="font-weight:700;color:#FFFFFF;font-size:0.95rem">{profile['full_name']}</div>
          <div style="font-size:0.72rem;margin-top:3px">
            <span style="background:{rc};color:white;padding:2px 8px;border-radius:20px;font-weight:600;font-size:0.68rem;letter-spacing:0.04em">{role_labels.get(role,'').upper()}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="color:#4B5563;font-size:0.68rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px">MENÚ</div>', unsafe_allow_html=True)

        page = st.session_state.get("page", "dashboard")

        nav_items = [
            ("dashboard", "🏠", "Inicio"),
            ("manual", "📖", "Manual"),
            ("guide", "🗂️", "Guía de Preguntas"),
            ("trainer", "🤖", "Entrenador Virtual"),
        ]
        if role in ("manager", "director"):
            nav_items.append(("admin", "⚙️", "Panel de Admin"))

        for page_id, icon, label in nav_items:
            is_active = page == page_id
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state["page"] = page_id
                st.rerun()

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        from utils.notifications import get_unread_count
        count = get_unread_count(profile["id"])
        badge = f" ({count})" if count > 0 else ""
        notif_label = f"🔔  Notificaciones{badge}"
        is_notif = page == "notifications"
        if st.button(notif_label, key="nav_notifications", use_container_width=True,
                     type="primary" if is_notif else "secondary"):
            st.session_state["page"] = "notifications"
            st.rerun()

        st.markdown('<div style="flex:1;min-height:40px"></div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪  Cerrar sesión", use_container_width=True):
            from auth import logout
            logout()
            st.session_state.clear()
            st.rerun()


def _page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin-bottom:24px">
      <h2 style="margin:0;color:#111111;font-weight:800">{title}</h2>
      {"<p style='margin:4px 0 0;color:#6B7280;font-size:0.9rem'>" + subtitle + "</p>" if subtitle else ""}
      <div style="height:3px;width:48px;background:#CC1414;border-radius:2px;margin-top:10px"></div>
    </div>""", unsafe_allow_html=True)


def main():
    from auth import is_logged_in, get_profile, get_role

    if not is_logged_in():
        render_login()
        return

    profile = get_profile()
    role = get_role()
    if not profile:
        render_login()
        return

    render_sidebar(profile, role)

    # Inyectar header helper en session_state para que las páginas lo usen
    st.session_state["_page_header"] = _page_header

    page = st.session_state.get("page", "dashboard")

    if page == "dashboard":
        from app_pages import dashboard; dashboard.render()
    elif page == "manual":
        from app_pages import manual; manual.render()
    elif page == "guide":
        from app_pages import guide; guide.render()
    elif page == "trainer":
        from app_pages import trainer; trainer.render()
    elif page == "admin":
        if role in ("manager", "director"):
            from app_pages import admin; admin.render()
        else:
            st.error("Sin acceso.")
    elif page == "notifications":
        from app_pages import notifications; notifications.render()
    else:
        from app_pages import dashboard; dashboard.render()


main()
