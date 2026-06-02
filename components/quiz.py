import streamlit as st


def render_quiz(questions: list[dict], section_id: int) -> tuple[dict, int] | None:
    """
    Renderiza el quiz de una sección.
    Retorna (quiz_answers, score_pct) si se completó, None si aún no.
    """
    if not questions:
        st.info("Esta sección no tiene quiz asignado.")
        return {}, 100

    quiz_key = f"quiz_state_{section_id}"
    submitted_key = f"quiz_submitted_{section_id}"

    if submitted_key in st.session_state:
        return st.session_state[submitted_key]

    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = {}

    st.markdown("### ✏️ Quiz de comprensión")
    st.markdown("Respondé las preguntas para completar la sección:")

    answers = {}
    all_answered = True

    for i, q in enumerate(questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        options = q.get("options", [])
        key = f"q_{section_id}_{i}"
        choice = st.radio(
            label=f"Pregunta {i+1}",
            options=options,
            key=key,
            label_visibility="collapsed",
            index=None
        )
        if choice is None:
            all_answered = False
        else:
            answers[str(i)] = options.index(choice)
        st.markdown("---")

    if st.button("✅ Enviar respuestas", disabled=not all_answered, use_container_width=True):
        correct = 0
        for i, q in enumerate(questions):
            if answers.get(str(i)) == q.get("correct", 0):
                correct += 1
        score = int((correct / len(questions)) * 100)
        result = (answers, score)
        st.session_state[submitted_key] = result
        return result

    if not all_answered:
        st.caption("Respondé todas las preguntas para continuar.")

    return None


def show_quiz_result(score: int, correct: int, total: int):
    if score >= 75:
        st.success(f"🎉 ¡Muy bien! Respondiste {correct}/{total} correctas — **{score}%**")
    elif score >= 50:
        st.warning(f"📝 Bastante bien. Respondiste {correct}/{total} correctas — **{score}%**")
    else:
        st.error(f"📖 Repasá la sección. Respondiste {correct}/{total} correctas — **{score}%**")
