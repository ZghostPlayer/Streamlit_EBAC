# Imports
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Configuração inicial da página
st.set_page_config(
    page_title='Telemarketing Analysis',
    page_icon='telmarketing_icon.png',
    layout="wide",
    initial_sidebar_state='expanded'
)

# Configuração do tema para os gráficos
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Função para carregar os dados
@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para aplicar filtro de múltipla seleção
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados and len(selecionados) > 1:
        selecionados.remove('all')  # Remove 'all' se outros valores forem selecionados
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

# Função para converter o DataFrame para Excel
@st.cache_resource
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Função principal
def main():
    # Título principal da aplicação
    st.write('# Telemarketing Analysis')
    st.markdown("---")
    
    # Apresentar a imagem na barra lateral
    try:
        image = Image.open("Bank-Branding.jpg")
        st.sidebar.image(image)
    except FileNotFoundError:
        st.sidebar.warning("Imagem não encontrada!")

    # Upload do arquivo
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    # Verificar se o arquivo foi carregado
    if data_file_1 is not None:
        bank_raw = load_data(data_file_1)
        if bank_raw is None:
            return

        bank = bank_raw.copy()

        st.write('## Dados Antes dos Filtros')
        st.write(bank_raw.head())

        # Criar os filtros
        with st.sidebar.form(key='my_form'):
            graph_type = st.radio('Tipo de gráfico:', ('Barras', 'Pizza'))

            # Filtro de Idades
            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider(
                label='Idade',
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age),
                step=1
            )

            # Filtros de múltipla seleção
            filters = {
                "Profissão": "job",
                "Estado Civil": "marital",
                "Default": "default",
                "Tem financiamento imobiliário?": "housing",
                "Tem empréstimo?": "loan",
                "Meio de contato": "contact",
                "Mês do contato": "month",
                "Dia da semana": "day_of_week",
            }

            selected_filters = {}
            for label, column in filters.items():
                options = bank[column].unique().tolist()
                options.append('all')
                selected = st.multiselect(label, options, default=['all'])
                selected_filters[column] = selected

            # Aplicar os filtros
            bank = bank.query("age >= @idades[0] and age <= @idades[1]")
            for column, selected in selected_filters.items():
                bank = multiselect_filter(bank, column, selected)

            submit_button = st.form_submit_button(label='Aplicar')

        # Exibir os dados filtrados
        st.write('## Dados Após os Filtros')
        if bank.empty:
            st.warning("Nenhum dado encontrado após aplicar os filtros.")
            return
        st.write(bank.head())
        st.markdown("---")

        # Download dos dados filtrados
        df_xlsx = to_excel(bank)
        st.download_button(
            label='📥 Download tabela filtrada em EXCEL',
            data=df_xlsx,
            file_name='bank_filtered.xlsx'
        )
        st.markdown("---")

        # Gráficos
        if graph_type == 'Barras':
            st.write("### Gráficos de Barras")
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
            ax[0].set_title('Dados Brutos')

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
            ax[1].set_title('Dados Filtrados')

            st.pyplot(fig)
        
        elif graph_type == 'Pizza':
            st.write("### Gráficos de Pizza")
            fig, ax = plt.subplots(1, 2, figsize=(10, 5))

            # Dados brutos
            bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True).mul(100)
            ax[0].pie(
                bank_raw_target_perc,
                labels=bank_raw_target_perc.index,
                autopct='%1.1f%%',
                colors=['blue', 'orange']
            )
            ax[0].set_title('Dados Brutos')

            # Dados filtrados
            bank_target_perc = bank['y'].value_counts(normalize=True).mul(100)
            ax[1].pie(
                bank_target_perc,
                labels=bank_target_perc.index,
                autopct='%1.1f%%',
                colors=['blue', 'orange']
            )
            ax[1].set_title('Dados Filtrados')

            st.pyplot(fig)

if __name__ == '__main__':
    main()
