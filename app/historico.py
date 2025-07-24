import streamlit as st
import pandas as pd
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:5000/listar"  # 👉 Coloca aqui o IP do servidor Flask, se estiver em outro PC

def pegar_dados_historicos():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            dados = response.json()
            # Banco tem colunas: id, temperatura, umidade, horario
            df = pd.DataFrame(dados, columns=["ID", "Temperatura (°C)", "Umidade (%)", "Data/Hora"])
            df["Data/Hora"] = pd.to_datetime(df["Data/Hora"])
            df["Data"] = df["Data/Hora"].dt.date  # Só a data, sem hora

            # Agrupar por dia (média diária)
            df_agg = df.groupby("Data").agg({
                "Temperatura (°C)": "mean",
                "Umidade (%)": "mean"
            }).reset_index()

            return df_agg.tail(10)  # Últimos 10 dias
        else:
            st.error("Erro ao buscar dados. Código: " + str(response.status_code))
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")
        return pd.DataFrame()

def view_historico():
    st.title("📊 Histórico de Temperatura e Umidade")

    df = pegar_dados_historicos()

    if df.empty:
        st.warning("Sem dados para exibir.")
        return

    df["Data"] = pd.to_datetime(df["Data"])  # Garante formato de data pro gráfico

    st.line_chart(df.set_index("Data"))

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
