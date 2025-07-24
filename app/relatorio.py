import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

API_URL = "http://#urlServerFlask/listar"  # Coloca a URL real aqui!

def pegar_dados():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            dados = response.json()
            registros = dados[-20:]  # Pega os últimos 20
            df = pd.DataFrame(registros, columns=[
                "ID", "Temperatura Ar (°C)", "Umidade Ar (%)",
                "Umidade Solo (%)", "Chuva", "Data/Hora"
            ])
            df["Data/Hora"] = pd.to_datetime(df["Data/Hora"])
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()

def analisar_impacto(df):
    faixa_temp = (29.0, 32.0)
    faixa_umid_ar = (75.0, 90.0)
    faixa_umid_solo = (75.0, 90.0)

    temp_fora = df[~df["Temperatura Ar (°C)"].between(*faixa_temp)]
    umid_ar_fora = df[~df["Umidade Ar (%)"].between(*faixa_umid_ar)]
    umid_solo_fora = df[~df["Umidade Solo (%)"].between(*faixa_umid_solo)]

    total = len(df)
    risco_temp = len(temp_fora) / total * 100
    risco_umid_ar = len(umid_ar_fora) / total * 100
    risco_umid_solo = len(umid_solo_fora) / total * 100

    media_temp = df["Temperatura Ar (°C)"].mean()
    media_umid_ar = df["Umidade Ar (%)"].mean()
    media_umid_solo = df["Umidade Solo (%)"].mean()
    vezes_choveu = df["Chuva"].sum()

    risco_total = (risco_temp + risco_umid_ar + risco_umid_solo) / 3

    if risco_total < 25:
        impacto = "Baixo Impacto"
        cor = "green"
    elif risco_total < 60:
        impacto = "Médio Impacto"
        cor = "orange"
    else:
        impacto = "Alto Impacto"
        cor = "red"

    return impacto, cor, risco_total, media_temp, media_umid_ar, media_umid_solo, vezes_choveu, temp_fora, umid_ar_fora, umid_solo_fora

def view_relatorio():
    st.title("📋 Relatório de Impacto Ambiental")

    df = pegar_dados()
    if df.empty:
        st.warning("Nenhum dado disponível para análise.")
        return

    impacto, cor, risco_total, media_temp, media_umid_ar, media_umid_solo, vezes_choveu, temp_fora, umid_ar_fora, umid_solo_fora = analisar_impacto(df)

    st.subheader("📌 Análise Geral")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🌡️ Média Temp. Ar", value=f"{media_temp:.2f} °C")
        st.metric(label="🚨 Fora da Faixa (Temp)", value=f"{len(temp_fora)} registros")
    with col2:
        st.metric(label="💧 Média Umidade Ar", value=f"{media_umid_ar:.2f} %")
        st.metric(label="🚨 Fora da Faixa (Umi. Ar)", value=f"{len(umid_ar_fora)} registros")
    with col3:
        st.metric(label="🌱 Média Umidade Solo", value=f"{media_umid_solo:.2f} %")
        st.metric(label="🚨 Fora da Faixa (Umi. Solo)", value=f"{len(umid_solo_fora)} registros")

    st.subheader("🌧️ Ocorrência de Chuva")
    st.info(f"☔ Houve chuva em **{vezes_choveu} de {len(df)}** registros analisados.")

    st.subheader("📊 Classificação de Impacto")
    st.markdown(f"<h3 style='color:{cor};'>{impacto}</h3>", unsafe_allow_html=True)

    st.subheader("📈 Histograma das Temperaturas do Ar")
    fig, ax = plt.subplots()
    ax.hist(df["Temperatura Ar (°C)"], bins=10, color=cor, alpha=0.7)
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Frequência")
    ax.set_title("Distribuição de Temperaturas")
    st.pyplot(fig)

    st.info("📌 Faixa ideal: Temperatura 29–32°C | Umidade 75–90% (ar e solo)")

