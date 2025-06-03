import streamlit as st
from view import view_relatorio, side_bar
from view_data import view_data
from __init__ import main_view  
from historico import view_historico
from relatorio import view_relatorio

def main():
    
    opcao = side_bar() 
    main = st.empty()
    with main.container():

        if opcao == "Dados em Tempo Real":
            view_data()
        elif opcao == "Histórico":
            view_historico()
        elif opcao == "Relatório de Impacto":
            view_relatorio()
        elif opcao == "Menu":
            main_view()

if __name__ == "__main__":
    main()