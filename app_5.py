import timeit
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Configuração personalizada para gráficos
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Função para carregar dados com cache
@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para aplicar filtros de múltipla seleção
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados and len(selecionados) > 1:
        selecionados.remove('all')  # Remove 'all' se outras opções forem selecionadas
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

# Função principal
def main():
    # Configuração da página
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

    # Upload de arquivo
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    if data_file_1 is not None:
        # Medir tempo de carregamento do arquivo
        start = timeit.default_timer()
        bank_raw = load_data(data_file_1)
        load_time = timeit.default_timer() - start

        if bank_raw is None:
            return  # Termina se os dados não forem carregados

        st.write(f"Tempo de carregamento: {load_time:.2f} segundos")
        bank = bank_raw.copy()

        st.write('## Dados Antes dos Filtros')
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

            # Filtro de profissões
            jobs_list = bank.job.unique().tolist()
            jobs_list.append('all')
            jobs_selected = st.multiselect("Profissão", jobs_list, ['all'])

            # Filtro de estado civil
            marital_list = bank.marital.unique().tolist()
            marital_list.append('all')
            marital_selected = st.multiselect("Estado civil", marital_list, ['all'])

            # Filtro de default
            default_list = bank.default.unique().tolist()
            default_list.append('all')
            default_selected = st.multiselect("Default", default_list, ['all'])

            # Filtro de financiamento imobiliário
            housing_list = bank.housing.unique().tolist()
            housing_list.append('all')
            housing_selected = st.multiselect("Tem financiamento imobiliário?", housing_list, ['all'])

            # Filtro de empréstimos
            loan_list = bank.loan.unique().tolist()
            loan_list.append('all')
            loan_selected = st.multiselect("Tem empréstimo?", loan_list, ['all'])

            # Filtro de meio de contato
            contact_list = bank.contact.unique().tolist()
            contact_list.append('all')
            contact_selected = st.multiselect("Meio de contato", contact_list, ['all'])

            # Filtro de mês de contato
            month_list = bank.month.unique().tolist()
            month_list.append('all')
            month_selected = st.multiselect("Mês do contato", month_list, ['all'])

            # Filtro de dia da semana
            day_of_week_list = bank.day_of_week.unique().tolist()
            day_of_week_list.append('all')
            day_of_week_selected = st.multiselect("Dia da semana", day_of_week_list, ['all'])

            # Aplicar filtros
            bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                        .pipe(multiselect_filter, 'job', jobs_selected)
                        .pipe(multiselect_filter, 'marital', marital_selected)
                        .pipe(multiselect_filter, 'default', default_selected)
                        .pipe(multiselect_filter, 'housing', housing_selected)
                        .pipe(multiselect_filter, 'loan', loan_selected)
                        .pipe(multiselect_filter, 'contact', contact_selected)
                        .pipe(multiselect_filter, 'month', month_selected)
                        .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
                    )

            submit_button = st.form_submit_button(label='Aplicar')

        st.write('## Dados Após os Filtros')
        if bank.empty:
            st.warning("Nenhum dado encontrado após aplicar os filtros.")
            return
        st.write(bank.head())
        st.markdown("---")

        # Gráficos
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

        st.pyplot(fig)

if __name__ == '__main__':
    main()
