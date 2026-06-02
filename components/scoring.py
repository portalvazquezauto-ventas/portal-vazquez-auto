import streamlit as st
import pandas as pd


def score_color(score: int | None) -> str:
    if score is None:
        return "#9CA3AF"
    if score >= 75:
        return "#16A34A"
    if score >= 50:
        return "#D97706"
    return "#CC1414"


def score_badge(score: int | None, label: str = "") -> str:
    color = score_color(score)
    val = f"{score}%" if score is not None else "—"
    return f'<span style="background:{color};color:white;padding:3px 10px;border-radius:12px;font-weight:600;font-size:0.85rem">{label}{val}</span>'


def render_score_cards(scores: dict):
    """Muestra tarjetas de score para indagación, objeciones, consultivo, global."""
    labels = {
        "indagacion": "Indagación",
        "objeciones": "Objeciones",
        "consultivo": "Consultivo",
        "global": "Score Global",
    }
    cols = st.columns(len(scores))
    for col, (key, label) in zip(cols, labels.items()):
        val = scores.get(key)
        color = score_color(val)
        with col:
            st.markdown(
                f"""<div style="text-align:center;padding:12px;border-radius:10px;border:2px solid {color}">
                <div style="font-size:0.8rem;color:#6B7280;margin-bottom:4px">{label}</div>
                <div style="font-size:2rem;font-weight:700;color:{color}">{val if val is not None else '—'}</div>
                </div>""",
                unsafe_allow_html=True
            )


def style_score_dataframe(df: pd.DataFrame, score_cols: list[str]) -> pd.DataFrame.style:
    """Aplica colores condicionales a columnas de score en un DataFrame."""
    def color_cell(val):
        try:
            v = int(val)
        except (TypeError, ValueError):
            return ""
        if v >= 75:
            return "background-color:#D1FAE5;color:#065F46;font-weight:600"
        if v >= 50:
            return "background-color:#FEF3C7;color:#92400E;font-weight:600"
        return "background-color:#FEE2E2;color:#991B1B;font-weight:600"

    styler = df.style
    for col in score_cols:
        if col in df.columns:
            # pandas >= 2.1 renombró applymap → map
            if hasattr(styler, "map"):
                styler = styler.map(color_cell, subset=[col])
            else:
                styler = styler.applymap(color_cell, subset=[col])
    return styler


def render_progress_bar(value: int, label: str = "", color: str | None = None):
    c = color or score_color(value)
    st.markdown(
        f"""<div style="margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;margin-bottom:2px">
          <span style="font-size:0.85rem">{label}</span>
          <span style="font-size:0.85rem;font-weight:600;color:{c}">{value}%</span>
        </div>
        <div style="background:#E5E7EB;border-radius:6px;height:8px">
          <div style="background:{c};width:{value}%;height:8px;border-radius:6px"></div>
        </div></div>""",
        unsafe_allow_html=True
    )
