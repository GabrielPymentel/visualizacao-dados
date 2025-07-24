import streamlit as st
import pandas as pd
import requests

# Coloca o IP certo aqui
API_URL = "http://127.0.0.1:5000/listar"  
# Ex: http://192.168.0.52:5000/listar se a API estiver em outro PC

def pegar_dados_recentes():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            dados = response.json()
            registros = dados[-10:]  # últimos 10 registros
            df = pd.DataFrame(registros, columns=["ID", "Temperatura (°C)", "Umidade (%)", "Data/Hora"])
            df["Data/Hora"] = pd.to_datetime(df["Data/Hora"])
            return df
        else:
            st.error(f"Erro ao buscar dados. Status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()

def main_view():
    st.title("🌍 Bem-Vindo ao Sistema de Visualização")

    st.subheader("📊 Interface Interativa para Monitoramento Ambiental")
    st.write("""
        Este sistema permite a visualização de dados de sensores de temperatura e umidade do ar e solo, 
        ajudando no controle de chocadeiras de quelônios. Com ele, você pode:

        ✅ **Monitorar dados em tempo real**  
        📈 **Visualizar históricos e tendências**  
        🔔 **Receber alertas automáticos sobre variações perigosas**  
        📊 **Analisar gráficos e relatórios de impacto ambiental**  
    """)

    st.divider()

    st.subheader("📈 Últimas Leituras (Temperatura e Umidade do Ar)")

    df = pegar_dados_recentes()
    if not df.empty:
        st.line_chart(df.set_index("Data/Hora")[["Temperatura (°C)", "Umidade (%)"]])
        st.success("✅ Gráfico gerado com os últimos dados disponíveis.")
    else:
        st.warning("Nenhum dado encontrado para exibir o gráfico.")

    st.info("🔍 Explore as opções no menu lateral para visualizar os dados detalhados.")
