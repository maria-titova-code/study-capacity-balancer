import numpy as np
import pandas as pd
import streamlit as st
import math

def render_forgetting_curves(topics: list):
    #Строит график экспоненциального забывания для всех тем на 14 дней вперед.
    if not topics:
        st.info("Добавьте темы, чтобы увидеть график забывания.")
        return

    days_range = np.linspace(0, 14, 100)
    chart_data = {"Дни": days_range}

    for t in topics:
        S = t.get("stability", 2.0)
        #Формула: R(t) = exp(-t / S)
        retention_values = [math.exp(-d / S) * 100 for d in days_range]
        chart_data[t["name"]] = retention_values

    df = pd.DataFrame(chart_data).set_index("Дни")
    
    st.subheader("📈 Кривые забывания Эббингауза")
    st.caption("График показывает, как снижается процент помнимости материала в течение 14 дней.")
    st.line_chart(df)
