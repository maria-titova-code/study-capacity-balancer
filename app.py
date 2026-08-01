import streamlit as st
import pandas as pd
from decay_model import MemoryDecayModel
from optimizer import StudyOptimizer, Topic

import json
import os

DATA_FILE = "topics.json"

def load_topics():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {"name": "Матанализ: Пределы", "days": 5.0, "stability": 2.0, "cost": 30},
        {"name": "Физика: Законы Ньютона", "days": 7.0, "stability": 1.5, "cost": 40},
    ]

def save_topics(topics):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    
#1. Настройка страницы
st.set_page_config(
    page_title="Интервал",
    page_icon="📚",
    layout="centered"
)
st.title("📚 Интервал")
st.caption("Персональный оптимизатор учебной нагрузки на основе модели Эббингауза")

with st.expander("💡 Как это работает? (Инструкция)", expanded=False):
    st.markdown("""
    ### 👋 Добро пожаловать в «Интервал»!
    **Как пользоваться:**
    1. **Добавьте темы** в список ниже, указав сколько дней не повторяли и время на повторение.
    2. **Задайте лимит времени** через боковую панель настроек (кнопка ☰ слева вверху).
    3. **Нажмите «Сформировать план»**: алгоритм рассчитает риск забывания каждой темы и подберёт идеальный список на сегодня.
    """)
#2. Инициализация хранилища
if "topics" not in st.session_state:
    st.session_state.topics = load_topics()

#3. Настройка лимита времени на день
st.sidebar.header("⚙️ Настройки нагрузки")
max_daily_minutes = st.sidebar.slider(
    "Дневной лимит времени (минуты):",
    min_value = 15,
    max_value = 180,
    value = 60,
    step = 15
)

#4. Форма для добавления тем
st.write("---")
st.subheader("➕ Добавить тему")

with st.form("add_topic_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Название темы", placeholder="Например: Линейная алгебра")
        days = st.number_input("Дней с последнего повторения", min_value=0.0, value=3.0, step=0.5)
    with col2:
        stability = st.number_input("Прочность памяти (S) (в днях)", min_value=0.5, value=2.0, step=0.5)
        cost = st.number_input("Время на повторение (минуты)", min_value=5, value=20, step=5)
    
    add_btn = st.form_submit_button("Добавить тему в список", use_container_width=True)
    if add_btn:
        if name.strip():
            # Добавляем тему и сразу сохраняем в файл
            st.session_state.topics.append({
                "name": name,
                "days": days,
                "stability": stability,
                "cost": cost
            })
            save_topics(st.session_state.topics)    
            st.success(f"Тема «{name}» успешно добавлена и сохранена.")
        else:
            st.warning("Введите название темы.")

#5. Список всех тем
st.write("---")
st.subheader("📋 Список ваших тем")

if st.session_state.topics:
    topics_df = pd.DataFrame([
        {
            "Тема": t["name"],
            "Дней прошло": t["days"],
            "Прочность (S)": t["stability"],
            "Время (минуты)": t["cost"]
        } for t in st.session_state.topics
    ])
    st.dataframe(topics_df, use_container_width=True)

    if st.button("🗑 Очистить все темы"):
        st.session_state.topics = []
        save_topics([])
        st.rerun()

    #6. Расчет оптимизации
    st.write("---")
    if st.button("🚀 Сформировать план на сегодня", type="primary", use_container_width=True):
        decay_model = MemoryDecayModel()
        optimizer = StudyOptimizer(decay_model)

        topic_objects = [
            Topic(t["name"], t["days"], t["stability"], t["cost"])
            for t in st.session_state.topics
        ]

        result = optimizer.optimize_daily_schedule(topic_objects, max_daily_minutes)

        st.subheader("🎯 Результаты оптимизации")
        
        percent_used = min(result['total_time_used'] / max_daily_minutes, 1.0)
        st.metric(
            label="Занято времени", 
            value=f"{result['total_time_used']} минут из {max_daily_minutes} минут"
        )
        st.progress(percent_used)

        res_col1, res_col2 = st.columns(2)

        with res_col1:
            st.markdown("### ✅ Включено в план")
            if result['scheduled_today']:
                for item in result['scheduled_today']:
                    with st.container(border=True):
                        st.markdown(f"**📌 {item['name']}**")
                        st.caption(f"⏱ Время: {item['cost_minutes']} мин.")
                        st.error(f"📉 Риск забывания: {item['forgetting_risk']}")
            else:
                st.info("Сегодня повторений не требуется!")

        with res_col2:
            st.markdown("### ⏳ Отложено на потом")
            if result['deferred_topics']:
                for item in result['deferred_topics']:
                    with st.container(border=True):
                        st.markdown(f"**📌 {item['name']}**")
                        st.caption("Не уместилось в дневной лимит")
                        st.warning(f"📉 Риск забывания: {item['forgetting_risk']}")
            else:
                st.success("Все темы уместились в план!")
else:
    st.info("Список тем пуст. Добавьте темы через форму выше!")
