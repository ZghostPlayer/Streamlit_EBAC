import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

def main():
    st.set_page_config(page_title='Telemarketing analisys', 
                       page_icon='../img/telmarketing_icon.png',
                       layout="wide",
                       initial_sidebar_state='expanded')

    st.write('# Telemarketing analisys')
    st.markdown("---")

    # Exibir imagem na barra lateral
    image = Image.open("../img/Bank-Branding.jpg")
    st.sidebar.image(image)

    # Ler dados
    bank_raw = pd.read_csv('../data/input/bank-additional-full.csv', sep=';')
    bank = bank_raw.copy()

    st.write('## Antes dos filtros')
    st.write(bank_raw.head())

    # Slider para idade
    max_age = int(bank.age.max())
    min_age = int(bank.age.min())
    idades = st.sidebar.slider(label='Idade', 
                                min_value=min_age,
                                max_value=max_age, 
                                value=(min_age, max_age),
                                step=1)
    st.sidebar.write('Idades selecionadas:', idades)

    # Aplicar filtro
    bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]

    if bank.empty:
        st.warning("Nenhum dado encontrado após os filtros.")
        return

    st.write('## Após os filtros')
    st.write(bank.head())
    st.markdown("---")

    # PLOTS    
    plt.clf()
    plt.close('all')
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

        # Gráfico dos dados brutos
    bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True).mul(100).reset_index()
    bank_raw_target_perc.columns = ['y', 'proportion']
    sns.barplot(
        x='y', 
        y='proportion', 
        data=bank_raw_target_perc, 
        ax=ax[0], 
        order=['no', 'yes'], 
        palette={'no': 'blue', 'yes': 'orange'}
    )
    for container in ax[0].containers:
        ax[0].bar_label(container)
    ax[0].set_title('Dados brutos', fontweight="bold")

    # Gráfico dos dados filtrados
    bank_target_perc = bank['y'].value_counts(normalize=True).mul(100).reset_index()
    bank_target_perc.columns = ['y', 'proportion']
    sns.barplot(
        x='y', 
        y='proportion', 
        data=bank_target_perc, 
        ax=ax[1], 
        order=['no', 'yes'], 
        palette={'no': 'blue', 'yes': 'orange'}
    )
    for container in ax[1].containers:
        ax[1].bar_label(container)
    ax[1].set_title('Dados filtrados', fontweight="bold")

    st.write('## Proporção de aceite')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
