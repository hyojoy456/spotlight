# Тестовое приложение на Streamlit (MCQ)

- 8 банков заданий + 1 общий тест.
- В админке можно вставлять задание формата: `1. Question ... a) opt1 b) opt2 c) opt3` и выбрать правильный ответ.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Деплой по ссылке

1. Залейте проект на GitHub.
2. Откройте Streamlit Cloud: https://share.streamlit.io
3. Подключите репозиторий, укажите команду запуска: `streamlit run app.py`.
4. Получите публичную ссылку.
