import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Configuração personalizada para os gráficos
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Função para filtro multiseleção
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados and len(selecionados) > 1:
        selecionados.remove('all')  # Remove 'all' se houver outros valores selecionados
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

# Função principal da aplicação
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

    # Carregar imagem para a barra lateral
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

    # Filtros na barra lateral
    with st.sidebar.form(key='my_form'):
        # Filtro de idade
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        idades = st.slider(
            label='Idade',
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
            step=1
        )
        st.write('Idades selecionadas:', idades)

        # Filtro de profissões
        jobs_list = bank.job.unique().tolist()
        jobs_list.append('all')
        jobs_selected = st.multiselect(
            "Profissões",
            options=jobs_list,
            default=['all']
        )
        st.write('Profissões selecionadas:', jobs_selected)

        # Aplicação dos filtros
        bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
        bank = multiselect_filter(bank, 'job', jobs_selected)

        submit_button = st.form_submit_button(label='Aplicar')

    # Verificar se o dataframe filtrado está vazio
    st.write('## Após os filtros')
    if bank.empty:
        st.warning("Nenhum dado encontrado após aplicar os filtros.")
        return
    st.write(bank.head())
    st.markdown("---")

    # Criar gráficos
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Gráfico dos dados brutos
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

    # Gráfico dos dados filtrados
    try:
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
    except KeyError:
        st.error("Erro ao gerar o gráfico filtrado. Verifique os dados aplicados.")

    # Exibir os gráficos
    st.write('## Proporção de Aceite')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
