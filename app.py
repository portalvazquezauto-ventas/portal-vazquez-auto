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

  /* ── Botón de reabrir sidebar — siempre visible ── */
  [data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 9999 !important;
    background: #CC1414 !important;
    border-radius: 8px !important;
    padding: 4px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
  }
  [data-testid="stSidebarCollapsedControl"] svg {
    fill: white !important;
    color: white !important;
  }
  [data-testid="stSidebarCollapsedControl"] button {
    color: white !important;
  }

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

  /* ── MOBILE ── */
  @media (max-width: 768px) {

    /* Contenido principal — más padding lateral */
    .block-container {
      padding: 1rem 0.75rem 5rem !important;
      max-width: 100% !important;
    }

    /* Sidebar colapsado por default en mobile — Streamlit ya lo maneja,
       pero ajustamos el botón de toggle para que sea visible */
    [data-testid="stSidebarCollapsedControl"] {
      top: 8px !important;
      left: 8px !important;
    }

    /* Headings más chicos */
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1rem !important; }

    /* Métricas — una por fila */
    [data-testid="stMetric"] {
      padding: 12px 14px !important;
    }

    /* Columnas — stack en mobile */
    [data-testid="stHorizontalBlock"] {
      flex-wrap: wrap !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
      min-width: 100% !important;
      flex: 1 1 100% !important;
    }

    /* Tabs — scroll horizontal */
    .stTabs [data-baseweb="tab-list"] {
      overflow-x: auto !important;
      flex-wrap: nowrap !important;
      -webkit-overflow-scrolling: touch;
    }
    .stTabs [data-baseweb="tab"] {
      white-space: nowrap !important;
      padding: 6px 12px !important;
      font-size: 0.82rem !important;
    }

    /* Cards del manual — full width */
    .vazquez-card { padding: 14px !important; }

    /* Chat input — más grande en mobile */
    [data-testid="stChatInput"] textarea {
      font-size: 1rem !important;
    }

    /* Botones — más fáciles de tocar */
    .stButton > button {
      min-height: 44px !important;
      font-size: 0.9rem !important;
    }

    /* Dataframe — scroll horizontal */
    .stDataFrame { overflow-x: auto !important; }

    /* Progress bar de manual */
    [data-testid="stProgress"] { margin: 4px 0 !important; }

    /* Ocultar scrollbar en mobile */
    ::-webkit-scrollbar { width: 0px; height: 0px; }
  }

  /* ── TABLET (768px–1024px) ── */
  @media (min-width: 769px) and (max-width: 1024px) {
    .block-container {
      padding: 1.5rem 1.5rem 2rem !important;
    }
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.3rem !important; }
  }
</style>
""", unsafe_allow_html=True)


def _logo_html(size: str = "normal") -> str:
    if size == "small":
        return """
        <div style="display:flex;align-items:center;gap:10px;padding:18px 0 14px">
          <div style="background:#CC1414;border-radius:8px;padding:5px 10px;display:inline-flex;
                      flex-direction:column;align-items:flex-start;line-height:1;
                      box-shadow:0 2px 8px rgba(204,20,20,0.3)">
            <span style="color:white;font-weight:900;font-size:0.92rem;letter-spacing:0.04em">VÁZQUEZ</span>
            <span style="color:rgba(255,255,255,0.75);font-weight:600;font-size:0.52rem;letter-spacing:0.25em">AUTO</span>
          </div>
          <div>
            <div style="color:#6B7280;font-size:0.65rem;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;margin-top:1px">
              Portal Comercial
            </div>
          </div>
        </div>"""
    return """
    <div style="text-align:center;padding:40px 0 28px">
      <div style="display:inline-flex;flex-direction:column;align-items:center;gap:12px">
        <div style="background:#CC1414;border-radius:14px;padding:14px 28px;
                    box-shadow:0 6px 24px rgba(204,20,20,0.4);display:inline-flex;
                    flex-direction:column;align-items:center;line-height:1;gap:4px">
          <span style="color:white;font-weight:900;font-size:2rem;letter-spacing:0.06em;
                       text-shadow:0 1px 3px rgba(0,0,0,0.2)">VÁZQUEZ</span>
          <span style="color:rgba(255,255,255,0.8);font-weight:700;font-size:0.85rem;
                       letter-spacing:0.35em">AUTO</span>
        </div>
        <div style="background:#F3F4F6;border-radius:20px;padding:4px 14px">
          <span style="color:#6B7280;font-size:0.78rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase">
            Portal Comercial Interno
          </span>
        </div>
      </div>
    </div>"""


def render_login():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    .block-container { max-width: 440px !important; padding-top: 3rem !important; }
    </style>""", unsafe_allow_html=True)

    st.markdown(_logo_html("normal"), unsafe_allow_html=True)

    # Modo: login o recuperar contraseña
    if st.session_state.get("show_reset"):
        _render_forgot_password()
        return

    # Input oculto para evitar tooltip "Press Enter to submit form" en el campo contraseña
    st.markdown("""
    <style>
    div[data-testid="stForm"] input[aria-label="__noop__"] {
      display:none !important; height:0 !important; padding:0 !important; border:none !important;
    }
    div[data-testid="stForm"] label:has(+ div input[aria-label="__noop__"]) { display:none !important; }
    </style>""", unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="tu@vazquezauto.com.ar")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")
        # Campo trampa: evita que el browser muestre "Press Enter to submit form" en el campo contraseña
        st.text_input("__noop__", label_visibility="collapsed", key="_noop_login")
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

    if st.button("¿Olvidaste tu contraseña?", use_container_width=True):
        st.session_state["show_reset"] = True
        st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:20px;color:#9CA3AF;font-size:0.75rem">
      © 2026 Vázquez Auto · Uso interno
    </div>""", unsafe_allow_html=True)


def _render_forgot_password():
    st.markdown("""
    <div style="background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;padding:16px 18px;margin-bottom:20px">
      <div style="font-weight:700;color:#92400E;margin-bottom:4px">🔑 Restablecer contraseña</div>
      <div style="color:#78350F;font-size:0.85rem">Te enviaremos un enlace a tu email para crear una nueva contraseña.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("reset_form"):
        email = st.text_input("Tu email", placeholder="tu@vazquezauto.com.ar")
        submit = st.form_submit_button("Enviar enlace →", use_container_width=True, type="primary")

        if submit:
            if not email:
                st.error("Ingresá tu email.")
            else:
                from auth import send_password_reset
                ok = send_password_reset(email)
                if ok:
                    st.success("✅ Revisá tu email — te enviamos el enlace para restablecer tu contraseña.")
                else:
                    st.error("No se pudo enviar el email. Contactá a tu encargado.")

    if st.button("← Volver al login"):
        st.session_state.pop("show_reset", None)
        st.rerun()


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


def _page_header(title: str, subtitle: str = "", show_back: bool = True):
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        st.markdown(
            '<div style="margin-bottom:4px">'
            '<h2 style="margin:0;color:#111111;font-weight:800">' + title + '</h2>'
            + ('<p style="margin:4px 0 0;color:#6B7280;font-size:0.9rem">' + subtitle + '</p>' if subtitle else '') +
            '<div style="height:3px;width:48px;background:#CC1414;border-radius:2px;margin-top:10px"></div>'
            '</div>',
            unsafe_allow_html=True
        )
    if show_back:
        with col_btn:
            st.markdown('<div style="padding-top:6px"></div>', unsafe_allow_html=True)
            if st.button("🏠 Inicio", key="_header_back_home", use_container_width=True):
                st.session_state["page"] = "dashboard"
                st.rerun()
    st.markdown('<div style="margin-bottom:20px"></div>', unsafe_allow_html=True)


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
