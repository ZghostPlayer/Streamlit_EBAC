import timeit
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Função para ler os dados com cache
@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para aplicar filtros de múltipla seleção
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados and len(selecionados) > 1:
        selecionados.remove('all')  # Remove 'all' se outras opções forem selecionadas
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

# Função para converter o DataFrame para string CSV
@st.cache_data
def df_to_string(df):
    return df.to_csv(index=False)

# Função para converter o DataFrame para Excel
@st.cache_resource
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def main():
    # Configuração inicial da página
    st.set_page_config(
        page_title='Telemarketing Analysis',
        page_icon='../img/telmarketing_icon.png',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    st.write('# Telemarketing Analysis')
    st.markdown("---")

    # Exibir imagem na barra lateral
    try:
        image = Image.open("../img/Bank-Branding.jpg")
        st.sidebar.image(image)
    except FileNotFoundError:
        st.sidebar.warning("Imagem não encontrada!")

    # Medir o tempo de carregamento do arquivo
    start = timeit.default_timer()
    bank_raw = load_data('../data/input/bank-additional-full.csv')
    load_time = timeit.default_timer() - start

    if bank_raw is None:
        st.warning("Nenhum dado foi carregado. Verifique o arquivo.")
        return

    st.write(f"Tempo de carregamento: {load_time:.2f} segundos")
    st.write('## Visualização dos Dados')
    st.write(bank_raw.head())

    # Converter DataFrame para CSV
    csv = df_to_string(bank_raw)
    st.write("### Download CSV")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='df_csv.csv',
        mime='text/csv'
    )

    # Converter DataFrame para Excel
    df_xlsx = to_excel(bank_raw)
    st.write("### Download Excel")
    st.download_button(
        label='📥 Download data as EXCEL',
        data=df_xlsx,
        file_name='df_excel.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.write(f'Tempo total: {timeit.default_timer() - start:.2f} segundos')

if __name__ == '__main__':
    main()
