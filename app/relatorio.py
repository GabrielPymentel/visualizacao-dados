
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

API_URL = "http://#urlServerFlask/listar"  # Atualize para a URL correta

def pegar_dados():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            dados = response.json()
            registros = dados[-20:]  # Pega os últimos 20 registros
            df = pd.DataFrame(registros, columns=["ID", "Temperatura (°C)", "Umidade (%)", "Data/Hora"])
            df["Data/Hora"] = pd.to_datetime(df["Data/Hora"])
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()

def analisar_impacto(df):
    # Faixas ideais segundo artigo
    faixa_temp = (29.0, 32.0)
    faixa_umid = (75.0, 90.0)

    temp_fora = df[~df["Temperatura (°C)"].between(*faixa_temp)]
    umid_fora = df[~df["Umidade (%)"].between(*faixa_umid)]

    total = len(df)
    risco_temp = len(temp_fora) / total * 100
    risco_umid = len(umid_fora) / total * 100
    media_temp = df["Temperatura (°C)"].mean()
    media_umid = df["Umidade (%)"].mean()

    risco_total = (risco_temp + risco_umid) / 2

    if risco_total < 25:
        impacto = "Baixo Impacto"
        cor = "green"
    elif risco_total < 60:
        impacto = "Médio Impacto"
        cor = "orange"
    else:
        impacto = "Alto Impacto"
        cor = "red"

    return impacto, cor, risco_total, media_temp, media_umid, temp_fora, umid_fora

def view_relatorio():
    st.title("📋 Relatório de Impacto Ambiental")

    df = pegar_dados()
    if df.empty:
        st.warning("Nenhum dado disponível para análise.")
        return

    impacto, cor, risco_total, media_temp, media_umid, temp_fora, umid_fora = analisar_impacto(df)

    st.subheader("📌 Análise Geral")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🌡️ Média Temp.", value=f"{media_temp:.2f} °C")
        st.metric(label="❄️ Fora da Faixa (Temp)", value=f"{len(temp_fora)} registros")
    with col2:
        st.metric(label="💧 Média Umidade", value=f"{media_umid:.2f} %")
        st.metric(label="🚨 Fora da Faixa (Umidade)", value=f"{len(umid_fora)} registros")

    st.subheader("📊 Classificação de Impacto")
    st.markdown(f"<h3 style='color:{cor};'>{impacto}</h3>", unsafe_allow_html=True)

    st.subheader("📈 Distribuição das Temperaturas")
    fig, ax = plt.subplots()
    ax.hist(df["Temperatura (°C)"], bins=10, color=cor, alpha=0.7)
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Frequência")
    ax.set_title("Histograma das Temperaturas")
    st.pyplot(fig)

    st.info("📌 Faixa ideal de temperatura: 29°C a 32°C | Umidade: acima de 75%")
