import timeit
import pandas as pd
import streamlit as st

# Função para ler os dados
@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho.")
        return None

def main():
    # Configuração inicial da página
    st.set_page_config(
        page_title="Telemarketing Analysis",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.write("# Telemarketing Analysis")
    st.markdown("---")

    # Medir tempo de carregamento do arquivo
    start = timeit.default_timer()
    bank_raw = load_data("../data/input/bank-additional-full-40.csv")
    load_time = timeit.default_timer() - start

    if bank_raw is not None:
        st.write(f"Tempo de carregamento: {load_time:.2f} segundos")
        st.write("## Dados Carregados")
        st.write(bank_raw.head())
    else:
        st.warning("Nenhum dado foi carregado. Verifique o arquivo.")

if __name__ == "__main__":
    main()
