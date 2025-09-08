import streamlit as st
from utils.bank import (
    BANK_NAMES,
    get_random_questions_from_bank,
    get_random_questions_from_multiple,
)

st.set_page_config(page_title="Тесты", page_icon="🧪", layout="wide")

if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "selected_bank" not in st.session_state:
    st.session_state.selected_bank = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}


def start_test_for_bank(bank_name: str, combined: bool = False) -> None:
    st.session_state.mode = "test"
    st.session_state.selected_bank = bank_name
    if combined:
        st.session_state.questions = get_random_questions_from_multiple(BANK_NAMES)
    else:
        st.session_state.questions = get_random_questions_from_bank(bank_name)
    st.session_state.current_index = 0
    st.session_state.answers = {}


def go_home() -> None:
    st.session_state.mode = "home"
    st.session_state.selected_bank = None
    st.session_state.questions = []
    st.session_state.current_index = 0
    st.session_state.answers = {}


st.markdown(
    """
    <style>
    .square-btn > button { width: 100%; height: 110px; border-radius: 12px; font-size: 20px; font-weight: 600; }
    .bottom-btn > button { width: 100%; height: 64px; border-radius: 12px; font-size: 18px; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)


if st.session_state.mode == "home":
    st.title("Главная")
    st.caption("Выберите тест. Нижняя кнопка — общий тест из всех банков.")

    bank_labels = [f"Банк {i}" for i in range(1, 9)]

    for row in range(2):
        cols = st.columns(4, gap="large")
        for col_idx in range(4):
            i = row * 4 + col_idx
            with cols[col_idx]:
                if st.button(
                    bank_labels[i],
                    key=f"bank_btn_{i}",
                    type="primary",
                    use_container_width=True,
                    help=f"Открыть {bank_labels[i]}",
                ):
                    start_test_for_bank(BANK_NAMES[i])

    st.divider()
    if st.button(
        "Общий тест (все банки)",
        key="combined_btn",
        type="secondary",
        use_container_width=True,
        help="Случайные задания из всех 8 банков",
    ):
        start_test_for_bank("combined", combined=True)

else:
    st.button("← На главную", on_click=go_home)

    questions = st.session_state.questions
    idx = st.session_state.current_index

    st.header("Тест")
    if not questions:
        st.info("В выбранном банке пока нет вопросов. Вернитесь на главную и добавьте их в разделе Admin.")
    else:
        total = len(questions)
        st.caption(f"Вопрос {idx + 1} из {total}")
        q = questions[idx]
        st.write(q.get("text", ""))

        key = f"answer_{idx}"
        if q.get("type") == "mcq" and q.get("options"):
            option_labels = [f"{opt['key']}) {opt['text']}" for opt in q["options"]]
            current = st.session_state.answers.get(idx)
            choice = st.radio(
                "Выберите один вариант",
                options=option_labels,
                index=option_labels.index(current) if current in option_labels else None,
            )
            if choice:
                st.session_state.answers[idx] = choice
        else:
            st.text_input("Ваш ответ (свободная форма)", key=key)

        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            st.button(
                "Назад",
                disabled=idx == 0,
                on_click=lambda: st.session_state.__setitem__("current_index", max(0, idx - 1)),
            )
        with col_next:
            if idx < total - 1:
                st.button(
                    "Далее",
                    on_click=lambda: st.session_state.__setitem__("current_index", min(total - 1, idx + 1)),
                )
            else:
                if st.button("Завершить тест"):
                    go_home()
