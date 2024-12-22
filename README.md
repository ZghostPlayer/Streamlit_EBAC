# Telemarketing Analysis

Este projeto é uma aplicação interativa desenvolvida com **Streamlit** para análise e visualização de dados de campanhas de telemarketing. Ele permite carregar, filtrar e visualizar dados de forma intuitiva, com suporte para download dos resultados filtrados.

🚀 **Deploy:** O aplicativo está disponível para uso em: [Telemarketing Analysis App](https://appebac-ogf3rtbtelgzuny9anzmuz.streamlit.app/)

---

## 🛠 Funcionalidades

- **Upload de Dados**: Suporte para arquivos `.csv` ou `.xlsx` contendo dados de campanhas de telemarketing.
- **Filtros Interativos**:
  - Idade (slider).
  - Múltiplas categorias, como profissão, estado civil, financiamento, etc.
- **Visualização de Dados**:
  - Gráficos de barras e pizza para análise de proporções.
- **Exportação**: Download dos dados filtrados no formato Excel.
- **Customização**: Personalização do tema dos gráficos com a biblioteca **Seaborn**.

---

## 📋 Pré-requisitos

- Bibliotecas utilizadas:
  - streamlit
  - pandas
  - seaborn
  - matplotlib
  - pillow
  - xlsxwriter

## 📈 Exemplos de Uso
**Upload de Dados**
Envie um arquivo .csv ou .xlsx contendo informações de campanhas de marketing, com colunas como:

- age (idade)
- job (profissão)
- marital (estado civil)
- housing (financiamento imobiliário)
- loan (empréstimos)
- y (resultado da campanha)

**Visualização**
- Gráficos de Barras: Visualize a proporção de resultados (sim/não) antes e depois de aplicar os filtros.
- Gráficos de Pizza: Explore a distribuição de categorias selecionadas.

**Download**
Baixe os dados filtrados como um arquivo Excel para análises futuras.

🖼 Layout do Aplicativo
<img src="https://user-images.githubusercontent.com/exemplo/layout.png" alt="Tela do Aplicativo" width="600">
