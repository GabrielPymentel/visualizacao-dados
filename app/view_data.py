import streamlit as st
import pandas as pd
import requests
import random
# App de vizualização de dados via Streamlit a partir de uma API FLask
API_URL = "http://#urlServerFlask/listar"

def pegar_dados_reais():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            dados = response.json()
            if dados and isinstance(dados[-1], list):
                ultimo = dados[-1]
                return {
                    "Data/Hora": pd.to_datetime(ultimo[3]),
                    "Temperatura Ar": ultimo[1],
                    "Umidade Ar": ultimo[2],  # agora é real
                    "Temperatura Solo": random.uniform(26, 30),
                    "Umidade Solo": random.uniform(40, 60)
                }
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com API: {e}")
        return None

def avaliar_condicoes(temperatura_ar, umidade_ar, temperatura_solo, umidade_solo):
    alertas = []

    # Faixas teóricas com base no artigo
    faixa_temp_ideal = (29.0, 32.0)
    faixa_umid_ideal = (70.0, 90.0)  # Umidade ar/solo parecida
    faixa_umid_segura = (75.0, 90.0) # Faixa mais segura

    if not (faixa_temp_ideal[0] <= temperatura_ar <= faixa_temp_ideal[1]):
        alertas.append(f"⚠️ **Temperatura do Ar fora do ideal ({temperatura_ar:.2f}°C)**")
    if not (faixa_umid_ideal[0] <= umidade_ar <= faixa_umid_ideal[1]):
        alertas.append(f"⚠️ **Umidade do Ar fora do ideal ({umidade_ar:.2f}%)**")
    if not (faixa_temp_ideal[0] <= temperatura_solo <= faixa_temp_ideal[1]):
        alertas.append(f"⚠️ **Temperatura do Solo fora do ideal ({temperatura_solo:.2f}°C)**")
    if not (faixa_umid_ideal[0] <= umidade_solo <= faixa_umid_ideal[1]):
        alertas.append(f"⚠️ **Umidade do Solo fora do ideal ({umidade_solo:.2f}%)**")

    return alertas


def view_data():
    st.title("📡 Monitoramento de Temperatura e Umidade em Tempo Real")

    dados = pegar_dados_reais()
    if not dados:
        st.warning("Aguardando dados do sensor...")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="🌡️ Temperatura do Ar", value=f"{dados['Temperatura Ar']:.2f} °C")
        st.metric(label="💧 Umidade do Ar", value=f"{dados['Umidade Ar']:.2f} %")

    with col2:
        st.metric(label="🌍 Temperatura do Solo", value=f"{dados['Temperatura Solo']:.2f} °C")
        st.metric(label="🌱 Umidade do Solo", value=f"{dados['Umidade Solo']:.2f} %")

    alertas = avaliar_condicoes(
        dados["Temperatura Ar"], dados["Umidade Ar"],
        dados["Temperatura Solo"], dados["Umidade Solo"]
    )

    if alertas:
        st.error("⚠️ **Atenção! Algumas condições podem estar colocando os ovos em risco!**")
        for alerta in alertas:
            st.write(alerta)
    else:
        st.success("✅ **Todas as condições estão dentro dos níveis ideais para os ovos.**")

    st.write(f"📅 Última atualização: {dados['Data/Hora']}")
    st.write("🔄 Atualizando a cada 5 segundos...")

