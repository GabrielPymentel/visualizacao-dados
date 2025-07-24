import streamlit as st
import pandas as pd
import requests
import random

# URL da API Flask
API_URL = "http://#urlServerFlask/listar"  # Substitui por IP correto

# Função para pegar os dados reais da API
def pegar_dados_reais():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            dados = response.json()
            if dados and isinstance(dados[-1], list):
                ultimo = dados[-1]
                return {
                    "Data/Hora": pd.to_datetime(ultimo[5]),
                    "Temperatura Ar": ultimo[1],
                    "Umidade Ar": ultimo[2],
                    "Umidade Solo": ultimo[3],
                    "Chuva": ultimo[4],
                    "Temperatura Solo": random.uniform(27, 31)  # ainda simulado
                }
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com API: {e}")
        return None

# Função para avaliar os dados e gerar alertas
def avaliar_condicoes(temperatura_ar, umidade_ar, temperatura_solo, umidade_solo):
    alertas = []

    faixa_temp_ideal = (29.0, 32.0)
    faixa_umid_ideal = (70.0, 90.0)

    if not (faixa_temp_ideal[0] <= temperatura_ar <= faixa_temp_ideal[1]):
        alertas.append(f"⚠️ **Temperatura do Ar fora do ideal ({temperatura_ar:.2f}°C)**")
    if not (faixa_umid_ideal[0] <= umidade_ar <= faixa_umid_ideal[1]):
        alertas.append(f"⚠️ **Umidade do Ar fora do ideal ({umidade_ar:.2f}%)**")
    if not (faixa_temp_ideal[0] <= temperatura_solo <= faixa_temp_ideal[1]):
        alertas.append(f"⚠️ **Temperatura do Solo fora do ideal ({temperatura_solo:.2f}°C)**")
    if not (faixa_umid_ideal[0] <= umidade_solo <= faixa_umid_ideal[1]):
        alertas.append(f"⚠️ **Umidade do Solo fora do ideal ({umidade_solo:.2f}%)**")

    return alertas

# Função principal do dashboard
def view_data():
    st.title("📡 Monitoramento Ambiental em Tempo Real")

    dados = pegar_dados_reais()
    if not dados:
        st.warning("Aguardando dados do sensor...")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="🌡️ Temperatura do Ar", value=f"{dados['Temperatura Ar']:.2f} °C")
        st.metric(label="💧 Umidade do Ar", value=f"{dados['Umidade Ar']:.2f} %")

    with col2:
        st.metric(label="🌍 Temperatura do Solo", value=f"{dados['Temperatura Solo']:.2f} °C (simulado)")
        st.metric(label="🌱 Umidade do Solo", value=f"{dados['Umidade Solo']:.2f} %")

    # 🌧️ Detecção de chuva
    if dados["Chuva"] == 1:
        st.warning("☔ **Está chovendo agora no ambiente monitorado.**")
    elif dados["Chuva"] == 0:
        st.info("🌤️ **Sem registro de chuva no momento.**")
    else:
        st.text("Estado da chuva desconhecido.")

    # Avaliação de condições
    alertas = avaliar_condicoes(
        dados["Temperatura Ar"], dados["Umidade Ar"],
        dados["Temperatura Solo"], dados["Umidade Solo"]
    )

    if alertas:
        st.error("⚠️ **Atenção! Algumas condições podem estar fora dos padrões ideais.**")
        for alerta in alertas:
            st.write(alerta)
    else:
        st.success("✅ **Tudo nos conformes! Ambiente ideal para incubação.**")

    st.write(f"📅 Última atualização: {dados['Data/Hora']}")
    st.write("🔄 Atualizando a cada 5 segundos...")

# Rodando o app
if __name__ == "__main__":
    view_data()
