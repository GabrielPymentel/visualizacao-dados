import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def pegar_dados_historicos():
    # Simulação de dados reais — depois substitui por uma chamada à API Flask
    hoje = datetime.today()
    datas = [hoje - timedelta(days=i) for i in range(9, -1, -1)]  # últimos 10 dias

    data = {
        "Data": [d.strftime("%Y-%m-%d") for d in datas],
        "Temperatura (°C)": [29.5, 30.2, 31.1, 28.7, 30.8, 32.3, 31.5, 29.9, 30.0, 28.9],
        "Umidade (%)": [78, 80, 76, 85, 82, 88, 70, 74, 77, 79]
    }

    return pd.DataFrame(data)

def view_historico():
    st.title("📊 Histórico de Temperatura e Umidade")

    df = pegar_dados_historicos()
    df["Data"] = pd.to_datetime(df["Data"])

    # Gráfico com Data como índice
    st.line_chart(df.set_index("Data"))

    # Destaques
    st.subheader("📌 Destaques do Histórico")
    col1, col2, col3 = st.columns(3)

    temp_max = df["Temperatura (°C)"].max()
    temp_min = df["Temperatura (°C)"].min()
    umidade_media = df["Umidade (%)"].mean()

    with col1:
        st.metric(label="🌡️ Máxima", value=f"{temp_max:.2f} °C")
    with col2:
        st.metric(label="❄️ Mínima", value=f"{temp_min:.2f} °C")
    with col3:
        st.metric(label="💧 Umidade Média", value=f"{umidade_media:.2f} %")

    st.info("📌 Temperaturas ideais para ovos de quelônios: 29°C a 32°C. Umidade ideal: acima de 75%.")
