import streamlit as st
import json
import re
from datetime import datetime
from auth import get_profile, is_manager_or_above
from supabase_client import get_client
from components.quiz import render_quiz, show_quiz_result
from utils.notifications import notify_manual_read


# ── Íconos por sección ──────────────────────────────────────────
SECTION_ICONS = {
    "1": "🎯", "2": "🏆", "3": "👥", "4": "🔄",
    "5": "🤝", "6": "📊", "7": "📈", "8": "⚙️",
    "9": "🚫", "10": "📋",
}

SECTION_COLORS = {
    "1": "#CC1414", "2": "#1D4ED8", "3": "#059669", "4": "#7C3AED",
    "5": "#D97706", "6": "#0891B2", "7": "#DC2626", "8": "#374151",
    "9": "#B91C1C", "10": "#4B5563",
}


def render():
    profile = get_profile()
    user_id = profile["id"]
    client = get_client()

    # Header de página
    st.markdown("""
    <div style="margin-bottom:32px">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
        <div style="background:#CC1414;color:white;width:40px;height:40px;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;font-size:1.3rem">📖</div>
        <div>
          <h2 style="margin:0;color:#111;font-weight:800">Manual de Ventas</h2>
          <p style="margin:0;color:#6B7280;font-size:0.85rem">Vázquez Auto · 2026</p>
        </div>
      </div>
      <div style="height:3px;width:48px;background:#CC1414;border-radius:2px;margin-top:6px"></div>
    </div>
    """, unsafe_allow_html=True)

    if is_manager_or_above():
        _render_update_button(profile, client)

    sections = _load_sections(client)
    if not sections:
        st.warning("No hay secciones cargadas. Un encargado debe actualizar el contenido desde Google Docs.")
        return

    reads = _load_my_reads(user_id, client)
    reads_by_section = {r["section_id"]: r for r in reads}

    _render_progress_visual(sections, reads_by_section)

    selected_id = st.session_state.get("selected_section")
    if selected_id:
        selected = next((s for s in sections if s["id"] == selected_id), None)
        if selected:
            if st.button("← Volver al índice", key="back_to_index"):
                st.session_state.pop("selected_section", None)
                st.session_state.pop(f"quiz_submitted_{selected_id}", None)
                st.rerun()
            _render_section_visual(selected, user_id, profile, reads_by_section, client)
            return

    _render_section_grid(sections, reads_by_section)


def _load_sections(client):
    try:
        return client.table("manual_sections").select("*").order("id").execute().data or []
    except Exception:
        return []


def _load_my_reads(user_id, client):
    try:
        return client.table("manual_reads").select("*").eq("user_id", user_id).execute().data or []
    except Exception:
        return []


# ── Barra de progreso visual ────────────────────────────────────
def _render_progress_visual(sections, reads_by_section):
    total = len(sections)
    completed = sum(1 for s in sections if reads_by_section.get(s["id"], {}).get("is_completed"))
    pct = int((completed / total) * 100) if total else 0

    avg_score = 0
    scores = [reads_by_section[s["id"]]["quiz_score"] for s in sections
              if reads_by_section.get(s["id"], {}).get("quiz_score") is not None]
    if scores:
        avg_score = int(sum(scores) / len(scores))

    avg_block = (
        '<div style="text-align:center">'
        '<div style="font-size:1.4rem;font-weight:800;color:#16A34A">' + str(avg_score) + '%</div>'
        '<div style="font-size:0.7rem;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.05em">Prom. Quiz</div>'
        '</div>'
    ) if scores else ""

    st.markdown(
        '<div style="background:white;border:1px solid #E5E7EB;border-radius:16px;padding:20px 24px;margin-bottom:28px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">'
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">'
        '<div>'
        '<span style="font-weight:700;color:#111;font-size:1rem">Tu progreso</span>'
        '<span style="color:#6B7280;font-size:0.85rem;margin-left:8px">' + str(completed) + ' de ' + str(total) + ' secciones completadas</span>'
        '</div>'
        '<div style="display:flex;gap:16px">'
        '<div style="text-align:center">'
        '<div style="font-size:1.4rem;font-weight:800;color:#CC1414">' + str(pct) + '%</div>'
        '<div style="font-size:0.7rem;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.05em">Avance</div>'
        '</div>'
        + avg_block +
        '</div>'
        '</div>', unsafe_allow_html=True)

    segments = "".join([
        '<div title="{}" style="flex:1;height:4px;border-radius:2px;background:{}"></div>'.format(
            s["title"],
            "#16A34A" if reads_by_section.get(s["id"], {}).get("is_completed") else "#E5E7EB"
        )
        for s in sections
    ])
    st.markdown(
        '<div style="background:white;border:1px solid #E5E7EB;border-radius:16px;padding:16px 24px 20px;margin-bottom:28px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">'
        '<div style="background:#F3F4F6;border-radius:999px;height:10px;overflow:hidden">'
        '<div style="background:linear-gradient(90deg,#CC1414,#E53E3E);height:100%;width:' + str(pct) + '%;border-radius:999px"></div>'
        '</div>'
        '<div style="display:flex;gap:4px;margin-top:10px">' + segments + '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ── Grid de secciones ───────────────────────────────────────────
def _render_section_grid(sections, reads_by_section):
    st.markdown('<div style="margin-bottom:16px"><span style="font-weight:700;color:#111;font-size:1.1rem">Secciones del manual</span></div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, section in enumerate(sections):
        read = reads_by_section.get(section["id"], {})
        is_done = read.get("is_completed", False)
        score = read.get("quiz_score")
        num = str(section["section_number"])
        icon = SECTION_ICONS.get(num, "📄")
        color = SECTION_COLORS.get(num, "#6B7280")

        score_badge = ""
        if score is not None:
            score_color = "#16A34A" if score >= 80 else "#D97706" if score >= 60 else "#DC2626"
            score_badge = f'<span style="background:{score_color}15;color:{score_color};padding:2px 8px;border-radius:12px;font-size:0.72rem;font-weight:700">{score}%</span>'

        status_bar = f'<div style="height:3px;background:{"#16A34A" if is_done else color};border-radius:2px;margin-bottom:12px"></div>'
        check = '<span style="color:#16A34A;font-size:0.9rem">✓ Completado</span>' if is_done else '<span style="color:#9CA3AF;font-size:0.85rem">Pendiente</span>'

        with cols[i % 2]:
            border_color = "#D1FAE5" if is_done else "#E5E7EB"
            icon_bg = color + "22"
            card_html = (
                '<div style="background:white;border:1px solid ' + border_color + ';border-radius:12px;'
                'padding:16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,0.04)">'
                + status_bar +
                '<div style="display:flex;align-items:flex-start;gap:10px">'
                '<div style="background:' + icon_bg + ';color:' + color + ';width:36px;height:36px;border-radius:8px;'
                'display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0">'
                + icon +
                '</div>'
                '<div style="flex:1;min-width:0">'
                '<div style="font-size:0.72rem;color:#9CA3AF;font-weight:600;letter-spacing:0.08em;text-transform:uppercase">Sección ' + num + '</div>'
                '<div style="font-weight:700;color:#111;font-size:0.9rem;line-height:1.3;margin-top:2px">' + section['title'] + '</div>'
                '<div style="display:flex;align-items:center;gap:8px;margin-top:8px">'
                + check + score_badge +
                '</div></div></div></div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"Abrir sección {num}", key=f"sec_{section['id']}", use_container_width=True, type="secondary"):
                st.session_state["selected_section"] = section["id"]
                st.rerun()


# ── Vista de sección ─────────────────────────────────────────────
def _render_section_visual(section, user_id, profile, reads_by_section, client):
    num = str(section["section_number"])
    icon = SECTION_ICONS.get(num, "📄")
    color = SECTION_COLORS.get(num, "#CC1414")
    read = reads_by_section.get(section["id"], {})

    # Header de sección
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{color}08,{color}15);border:1px solid {color}30;
                border-radius:16px;padding:24px;margin-bottom:24px">
      <div style="display:flex;align-items:center;gap:14px">
        <div style="background:{color};color:white;width:52px;height:52px;border-radius:12px;
                    display:flex;align-items:center;justify-content:center;font-size:1.6rem;flex-shrink:0">
          {icon}
        </div>
        <div>
          <div style="font-size:0.75rem;color:{color};font-weight:700;text-transform:uppercase;letter-spacing:0.08em">
            Sección {num}
          </div>
          <h2 style="margin:4px 0 0;color:#111;font-weight:800;font-size:1.4rem">{section['title']}</h2>
        </div>
        {"<div style='margin-left:auto;background:#D1FAE5;color:#16A34A;padding:6px 14px;border-radius:20px;font-weight:700;font-size:0.85rem'>✓ Completada</div>" if read.get("is_completed") else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if read.get("is_completed") and read.get("quiz_score") is not None:
        score = read["quiz_score"]
        sc = "#16A34A" if score >= 80 else "#D97706" if score >= 60 else "#DC2626"
        st.markdown(f"""
        <div style="background:{sc}10;border:1px solid {sc}30;border-radius:10px;
                    padding:12px 16px;margin-bottom:20px;display:flex;align-items:center;gap:10px">
          <span style="font-size:1.2rem">🏅</span>
          <span style="color:{sc};font-weight:700">Quiz completado con {score}%</span>
        </div>
        """, unsafe_allow_html=True)

    # Renderizar contenido visual
    _render_content_visual(section["content"], color)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("---")

    if not read.get("is_completed"):
        _ensure_read_started(user_id, section["id"], client)
        _render_quiz_section(section, user_id, profile, reads_by_section, client)


def _render_content_visual(content: str, accent_color: str):
    """Convierte markdown en bloques visuales atractivos."""
    lines = content.split("\n")
    blocks = _parse_content_blocks(lines)

    for block in blocks:
        btype = block["type"]

        if btype == "h1":
            pass  # Ya lo mostramos en el header de sección

        elif btype == "h2":
            st.markdown(f"""
            <div style="margin:28px 0 12px">
              <div style="display:flex;align-items:center;gap:8px">
                <div style="width:4px;height:20px;background:{accent_color};border-radius:2px"></div>
                <span style="font-weight:700;color:#111;font-size:1.05rem">{block['text']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        elif btype == "h3":
            st.markdown(f"""
            <div style="margin:20px 0 8px">
              <span style="font-weight:700;color:#374151;font-size:0.95rem;text-transform:uppercase;
                           letter-spacing:0.05em">{block['text']}</span>
            </div>
            """, unsafe_allow_html=True)

        elif btype == "rule":
            # Reglas / frases destacadas (texto entre **)
            st.markdown(f"""
            <div style="background:{accent_color}08;border-left:4px solid {accent_color};border-radius:0 12px 12px 0;
                        padding:16px 20px;margin:16px 0">
              <div style="font-weight:700;color:{accent_color};font-size:1rem;line-height:1.5">
                {block['text']}
              </div>
            </div>
            """, unsafe_allow_html=True)

        elif btype == "bullets":
            items_html = "".join([
                f'<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid #F3F4F6">'
                f'<div style="width:6px;height:6px;border-radius:50%;background:{accent_color};margin-top:7px;flex-shrink:0"></div>'
                f'<span style="color:#374151;font-size:0.9rem;line-height:1.5">{_inline_md(item)}</span>'
                f'</div>'
                for item in block["items"]
            ])
            st.markdown(f"""
            <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;
                        padding:4px 16px;margin:12px 0">
              {items_html}
            </div>
            """, unsafe_allow_html=True)

        elif btype == "numbered":
            items_html = "".join([
                f'<div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #F3F4F6">'
                f'<div style="background:{accent_color};color:white;width:22px;height:22px;border-radius:50%;'
                f'display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;flex-shrink:0">{j+1}</div>'
                f'<span style="color:#374151;font-size:0.9rem;line-height:1.5">{_inline_md(item)}</span>'
                f'</div>'
                for j, item in enumerate(block["items"])
            ])
            st.markdown(f"""
            <div style="background:white;border:1px solid #E5E7EB;border-radius:12px;
                        padding:4px 16px;margin:12px 0">
              {items_html}
            </div>
            """, unsafe_allow_html=True)

        elif btype == "callout":
            st.markdown(f"""
            <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;
                        padding:14px 18px;margin:12px 0;display:flex;gap:10px">
              <span style="font-size:1.1rem">💡</span>
              <span style="color:#92400E;font-size:0.9rem;line-height:1.5">{_inline_md(block['text'])}</span>
            </div>
            """, unsafe_allow_html=True)

        elif btype == "paragraph":
            text = block["text"].strip()
            if text:
                st.markdown(f"""
                <p style="color:#374151;font-size:0.92rem;line-height:1.7;margin:8px 0">{_inline_md(text)}</p>
                """, unsafe_allow_html=True)

        elif btype == "table":
            _render_visual_table(block["rows"], accent_color)

        elif btype == "chips":
            chips_html = "".join([
                f'<span style="background:{accent_color}12;color:{accent_color};padding:6px 14px;'
                f'border-radius:20px;font-size:0.82rem;font-weight:600;border:1px solid {accent_color}25">{c}</span>'
                for c in block["items"]
            ])
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0">{chips_html}</div>
            """, unsafe_allow_html=True)


def _parse_content_blocks(lines):
    """Agrupa líneas en bloques semánticos."""
    blocks = []
    i = 0
    bullet_buffer = []
    numbered_buffer = []
    para_buffer = []

    def flush_bullets():
        if bullet_buffer:
            blocks.append({"type": "bullets", "items": list(bullet_buffer)})
            bullet_buffer.clear()

    def flush_numbered():
        if numbered_buffer:
            blocks.append({"type": "numbered", "items": list(numbered_buffer)})
            numbered_buffer.clear()

    def flush_para():
        if para_buffer:
            text = " ".join(para_buffer).strip()
            if text:
                # Si es una frase en negrita sola → rule
                if re.match(r'^\*\*[^*]+\*\*$', text):
                    blocks.append({"type": "rule", "text": text.strip("*")})
                else:
                    blocks.append({"type": "paragraph", "text": text})
            para_buffer.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("# "):
            flush_bullets(); flush_numbered(); flush_para()
            blocks.append({"type": "h1", "text": stripped[2:].strip()})
        elif stripped.startswith("## "):
            flush_bullets(); flush_numbered(); flush_para()
            blocks.append({"type": "h2", "text": stripped[3:].strip()})
        elif stripped.startswith("### "):
            flush_bullets(); flush_numbered(); flush_para()
            blocks.append({"type": "h3", "text": stripped[4:].strip()})
        elif stripped.startswith("- ") or stripped.startswith("* "):
            flush_numbered(); flush_para()
            bullet_buffer.append(stripped[2:].strip())
        elif re.match(r'^\d+\.\s', stripped):
            flush_bullets(); flush_para()
            numbered_buffer.append(re.sub(r'^\d+\.\s', '', stripped))
        elif stripped == "" or stripped == "---":
            flush_bullets(); flush_numbered(); flush_para()
        else:
            flush_bullets(); flush_numbered()
            para_buffer.append(stripped)
        i += 1

    flush_bullets(); flush_numbered(); flush_para()
    return blocks


def _render_visual_table(rows, accent_color):
    if not rows:
        return
    header = rows[0]
    body = rows[1:]
    th_cells = "".join([f'<th style="padding:10px 14px;text-align:left;font-weight:700;color:white;background:{accent_color};font-size:0.82rem">{c}</th>' for c in header])
    tr_rows = ""
    for j, row in enumerate(body):
        bg = "#F9FAFB" if j % 2 == 0 else "white"
        td_cells = "".join([f'<td style="padding:10px 14px;font-size:0.85rem;color:#374151">{c}</td>' for c in row])
        tr_rows += f'<tr style="background:{bg}">{td_cells}</tr>'
    st.markdown(f"""
    <div style="overflow-x:auto;margin:12px 0;border-radius:10px;border:1px solid #E5E7EB;overflow:hidden">
      <table style="width:100%;border-collapse:collapse">
        <thead><tr>{th_cells}</tr></thead>
        <tbody>{tr_rows}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)


def _inline_md(text: str) -> str:
    """Convierte **bold** e *italic* a HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


# ── Quiz ─────────────────────────────────────────────────────────
def _render_quiz_section(section, user_id, profile, reads_by_section, client):
    questions = section.get("quiz_questions") or []
    if isinstance(questions, str):
        try:
            questions = json.loads(questions)
        except Exception:
            questions = []

    if questions:
        st.markdown(f"""
        <div style="background:#111;color:white;border-radius:16px;padding:20px 24px;margin-bottom:20px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
            <span style="font-size:1.2rem">🧠</span>
            <span style="font-weight:700;font-size:1rem">Quiz de la sección</span>
          </div>
          <p style="margin:0;color:#9CA3AF;font-size:0.85rem">
            Respondé las preguntas para completar esta sección.
          </p>
        </div>
        """, unsafe_allow_html=True)

    result = render_quiz(questions, section["id"])
    if result is not None:
        answers, score = result
        correct = sum(
            1 for i, q in enumerate(questions)
            if answers.get(str(i)) == q.get("correct", 0)
        )
        show_quiz_result(score, correct, len(questions))

        now = datetime.utcnow().isoformat()
        try:
            existing = client.table("manual_reads").select("id").eq("user_id", user_id).eq("section_id", section["id"]).execute().data
            payload = {"completed_at": now, "quiz_answers": answers, "quiz_score": score, "is_completed": True}
            if existing:
                client.table("manual_reads").update(payload).eq("id", existing[0]["id"]).execute()
            else:
                client.table("manual_reads").insert({"user_id": user_id, "section_id": section["id"], **payload}).execute()
        except Exception:
            pass

        notify_manual_read(
            user_id=user_id,
            user_name=profile["full_name"],
            section_title=section["title"],
            quiz_score=score,
            quiz_answers=answers,
            section_id=section["id"]
        )

        if st.button("➡️ Continuar al siguiente", type="primary"):
            st.session_state.pop("selected_section", None)
            st.session_state.pop(f"quiz_submitted_{section['id']}", None)
            st.rerun()


def _ensure_read_started(user_id, section_id, client):
    try:
        existing = client.table("manual_reads").select("id").eq("user_id", user_id).eq("section_id", section_id).execute().data
        if not existing:
            client.table("manual_reads").insert({"user_id": user_id, "section_id": section_id, "is_completed": False}).execute()
    except Exception:
        pass


def _render_update_button(profile, client):
    with st.expander("⚙️ Actualizar contenido del manual (desde Google Docs)"):
        st.warning("Esto actualiza todas las secciones y regenera los quizzes. No borra el historial de lecturas.")
        if st.button("🔄 Actualizar ahora"):
            with st.spinner("Leyendo Google Docs y regenerando quizzes..."):
                try:
                    from utils.google_docs import fetch_manual_from_google_docs
                    from utils.quiz_generator import generate_quiz_questions
                    sections = fetch_manual_from_google_docs()
                    for s in sections:
                        questions = generate_quiz_questions(s["title"], s["content"])
                        now = datetime.utcnow().isoformat()
                        existing = client.table("manual_sections").select("id").eq("section_number", s["section_number"]).execute().data
                        if existing:
                            client.table("manual_sections").update({
                                "title": s["title"], "content": s["content"],
                                "quiz_questions": questions, "last_updated": now,
                                "updated_by": profile["id"]
                            }).eq("id", existing[0]["id"]).execute()
                        else:
                            client.table("manual_sections").insert({
                                "section_number": s["section_number"], "title": s["title"],
                                "content": s["content"], "quiz_questions": questions,
                                "updated_by": profile["id"]
                            }).execute()
                    st.success(f"✅ {len(sections)} secciones actualizadas correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al actualizar: {e}")
