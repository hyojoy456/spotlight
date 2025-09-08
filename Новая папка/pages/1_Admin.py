import streamlit as st
from utils.bank import BANK_NAMES, add_text_question, add_mcq_question, parse_pasted_mcq, load_bank

st.set_page_config(page_title="Админ", page_icon="🛠", layout="wide")

st.title("Админка: добавление заданий")

bank_label_to_name = {f"Банк {i+1}": name for i, name in enumerate(BANK_NAMES)}
label = st.selectbox("Выберите банк", list(bank_label_to_name.keys()), index=0)
assert label is not None
bank_name = bank_label_to_name[label]

st.subheader("Добавить задание через вставку текста (MCQ)")
st.caption("Вставьте формат: 1. Question ... a) option1 b) option2 c) option3")

pasted = st.text_area("Вставьте задание", height=140, key="pasted")
if st.button("Распарсить"):
    q_text, opts = parse_pasted_mcq(pasted)
    if not q_text:
        st.error("Не удалось распарсить текст вопроса")
    elif len(opts) < 2:
        st.error("Найдено недостаточно вариантов. Убедитесь в формате a) b) c)")
    else:
        st.session_state.parsed_q = {"text": q_text, "options": opts}

if "parsed_q" in st.session_state:
    st.write("Предпросмотр:")
    st.write(st.session_state.parsed_q["text"])
    option_labels = [f"{o['key']}) {o['text']}" for o in st.session_state.parsed_q["options"]]
    correct_label = st.radio("Выберите правильный ответ", option_labels, key="correct_choice")
    if st.button("Сохранить в банк"):
        if not correct_label:
            st.error("Выберите правильный ответ")
        else:
            correct_key = correct_label.split(")")[0].strip()
            add_mcq_question(
                bank_name,
                st.session_state.parsed_q["text"],
                st.session_state.parsed_q["options"],
                correct_key,
            )
            st.success("Вопрос сохранён")
            del st.session_state.parsed_q

st.divider()

st.subheader("Добавить простой текстовый вопрос (без вариантов)")
with st.form("add_text_form", clear_on_submit=True):
    text = st.text_area("Текст задания", height=100)
    submitted = st.form_submit_button("Добавить в банк")
    if submitted:
        if not text.strip():
            st.error("Введите текст задания")
        else:
            add_text_question(bank_name, text.strip())
            st.success("Задание добавлено")

st.divider()

st.subheader("Текущие задания в выбранном банке")
questions = load_bank(bank_name)
if not questions:
    st.info("Пока нет заданий")
else:
    for q in questions:
        if q.get("type") == "mcq":
            opts = ", ".join([f"{o['key']}) {o['text']}" for o in q.get("options", [])])
            st.markdown(f"- [MCQ] {q['text']} — {opts} (верный: {q.get('correct_key')})")
        else:
            st.markdown(f"- {q.get('text', '')}")
