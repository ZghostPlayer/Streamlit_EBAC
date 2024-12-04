import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

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

    # Carregar dados
    try:
        bank_raw = pd.read_csv('../data/input/bank-additional-full.csv', sep=';')
        bank = bank_raw.copy()
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado!")
        return

    st.write('## Antes dos filtros')
    st.write(bank_raw.head())

    # Filtro por idade
    max_age = int(bank.age.max())
    min_age = int(bank.age.min())
    idades = st.sidebar.slider(
        label='Idade',
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        step=1
    )
    st.sidebar.write('Idades selecionadas:', idades)

    # Filtro por profissão
    jobs_list = bank.job.unique().tolist()
    jobs_selected = st.sidebar.multiselect(
        "Profissões",
        options=jobs_list,
        default=jobs_list
    )
    st.sidebar.write('Profissões selecionadas:', jobs_selected)

    # Aplicar filtros ao dataframe
    bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
    bank = bank[bank['job'].isin(jobs_selected)].reset_index(drop=True)

    st.write('## Após os filtros')
    if bank.empty:
        st.warning("Nenhum dado encontrado após aplicar os filtros.")
        return
    st.write(bank.head())
    st.markdown("---")

    # Criação dos gráficos
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Dados brutos
    bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True).mul(100).reset_index()
    bank_raw_target_perc.columns = ['y', 'proportion']
    sns.barplot(
        x='y',
        y='proportion',
        data=bank_raw_target_perc,
        ax=ax[0],
        palette={'no': 'blue', 'yes': 'orange'}
    )
    for container in ax[0].containers:
        ax[0].bar_label(container)
    ax[0].set_title('Dados Brutos', fontweight="bold")

    # Dados filtrados
    bank_target_perc = bank['y'].value_counts(normalize=True).mul(100).reset_index()
    bank_target_perc.columns = ['y', 'proportion']
    sns.barplot(
        x='y',
        y='proportion',
        data=bank_target_perc,
        ax=ax[1],
        palette={'no': 'blue', 'yes': 'orange'}
    )
    for container in ax[1].containers:
        ax[1].bar_label(container)
    ax[1].set_title('Dados Filtrados', fontweight="bold")

    # Exibir os gráficos
    st.write('## Proporção de Aceite')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
