import streamlit as st
import pandas as pd
import random
import time  

def gen_data():
    #Geração de dados
    agora = pd.to_datetime("now")
    return {
        "Data/Hora": agora,
        "Temperatura Ar": random.uniform(20.0, 30.0),
        "Umidade Ar": random.uniform(50.0, 80.0),
        "Temperatura Solo": random.uniform(15.0, 25.0),
        "Umidade Solo": random.uniform(30.0, 60.0)
    }  

def view_relatorio():
    st.title("Relatório de Impacto")
    st.write("Análise sobre o impacto da temperatura no desenvolvimento dos ovos.")

def side_bar():
    st.sidebar.title("Menu")
    opcao = st.sidebar.radio("Selecione uma opção:", 
                             ["Menu","Dados em Tempo Real", "Histórico", "Relatório de Impacto"])

    return opcao
