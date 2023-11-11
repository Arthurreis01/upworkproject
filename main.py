import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Adicionando conteúdo ao sidebar
st.set_page_config(layout="wide")

# Função para alternar entre os modos claro e escuro
def toggle_dark_mode():
    # Adiciona o botão ao lado do título
    button_clicked = st.button("🌙 Toggle Dark Mode")

    # Se o botão for clicado, altera o modo na variável de estado
    if button_clicked:
        st.session_state.dark_mode = not st.session_state.get("dark_mode", False)

    # Retorna o estado atual do modo escuro
    return st.session_state.get("dark_mode", False)

# Adicionando conteúdo à página
st.title('Interactive Graphics with Filters')

# Adiciona o botão de alternar modo claro/escuro
dark_mode = toggle_dark_mode()

# Aplica o tema escuro se o modo escuro estiver ativado
if dark_mode:
    st.markdown(
        """
        <style>
            body {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            .stApp {
                filter: invert(1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.write(" ")
st.write(" ")

# DATABASE (COLECT AND TREATMENT)
df = pd.read_csv("C:\\Users\\arthu\\Downloads\\data_for_dash.csv", sep=",")


df['ACTIVITY_DATE'] = pd.to_datetime(df['ACTIVITY_DATE'])

# Função para ordenar o DataFrame por 'ACTIVITY_DATE'
def sort_df_by_activity_date(dataframe):
    return dataframe.sort_values(by='ACTIVITY_DATE')

# 1. TOPIC BAR - FILL DATE BOXES

# 1.1 EXTRA EMPTY TABS
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns (3)

# 1.2 START DATE AND END DATE
with col1:
    start_date = st.date_input('Select Start Date')
with col3:
    end_date = st.date_input('Select End Date')

# Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# 1.3 FILTER DROPDOWN CAMPAIGN (BOX) - FILTER: MEDIA BUYER AND ACTIVE WITHIN (TODAY - DAYS)
with col2:
    media_buyer_filtered = st.selectbox("Select a media buyer", df['MEDIA_BUYER'].unique())
with col4:
    campaign_filtered = st.selectbox("Select a campaign", df['CAMPAIGN'].unique())

# 2 COLUMNS EXPECTED
filtered_df = df[(df['ACTIVITY_DATE'] >= start_date) & (df['ACTIVITY_DATE'] <= end_date) &
                 (df['CAMPAIGN'] == campaign_filtered) & (df['MEDIA_BUYER'] == media_buyer_filtered)]

group_of_days = st.slider('Filter by Group of Days', min_value=1, max_value=30, value=15)
with col5:
    active_within_days = st.slider('Active Within (Days)', min_value=1, max_value=31, value=30)

# graphics

# graphic 1 - line (Daily_Return)

# Somar os valores de "DAILY_RETURN" por data
summed_df = filtered_df.groupby('ACTIVITY_DATE')['DAILY_RETURN'].sum().reset_index()

# Criar o gráfico com Plotly Express
daily_fig = px.line(filtered_df, x="ACTIVITY_DATE", y="DAILY_RETURN", labels={'DAILY_RETURN': 'DAYLY_RETURN'})
st.plotly_chart(daily_fig, use_container_width=True)

total_return = px.bar(filtered_df,x="ACTIVITY_DATE", y="TOTAL_RETURN", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(total_return, use_container_width=True)

daily_profit = px.bar(filtered_df,x="ACTIVITY_DATE", y="DAILY_PROFIT", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(daily_profit, use_container_width=True)

total_profit = px.bar(filtered_df,x="ACTIVITY_DATE", y="TOTAL_PROFIT", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(total_profit, use_container_width=True)

spend_revenue = px.bar(filtered_df,x="ACTIVITY_DATE", y="REVENUE", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(spend_revenue, use_container_width=True)

# Verifique se as colunas estão presentes no DataFrame filtrado
required_columns = ['SPEND_PER_ARRIVAL', 'REVENUE_PER_ARRIVAL', 'PROFIT_PER_ARRIVAL']
if all(column in filtered_df.columns for column in required_columns):
    # Crie um gráfico de linhas usando plotly express
    line_chart = px.line(filtered_df, x='ACTIVITY_DATE', y=required_columns, labels={'value': 'Value', 'variable': 'Metric'},
                         title=f"Metrics Over Time - {media_buyer_filtered} - {campaign_filtered}")

    # Exiba o gráfico com largura total da página
    st.plotly_chart(line_chart, use_container_width=True)
else:
    st.warning(f"Columns {', '.join(required_columns)} not found in the filtered data.")


# Verifique se 'ACCEPTANCE_RATE' está presente no DataFrame filtrado
if 'ACCEPTANCE_RATE' in filtered_df.columns:
    # Calcule a média da ACCEPTANCE_RATE dentro do período filtrado
    average_acceptance_rate = filtered_df['ACCEPTANCE_RATE'].mean()

    # Exiba o valor médio em formato de texto com HTML para ajustar o estilo
    st.markdown(f'<div style="width:100%; text-align:center; font-size:54px;">'
                f'Average Acceptance Rate: {average_acceptance_rate:.2%}</div>', unsafe_allow_html=True)

    # Crie um widget st.metric para exibir o valor médio
    st.metric("Acceptance Rate (Average)", value=round(average_acceptance_rate, 4))
else:
    st.warning("Column 'ACCEPTANCE_RATE' not found in the filtered data.")

