import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout="wide")
# 1.1 create the pages
def campaign_stats_page():
    st.markdown("# Campaign Stats")
    # Add the content for the Campaign Stats page here
def page3():
    st.markdown("# Page3")
    # Add the content for Page3 here
def page4():
    st.markdown("# Page4")
    # Add the content for Page4 here

# 1.1.1 Setting button columns
col1, col2, col3 = st.columns(3)

if col1.button("Campaing Stats"):
    pagina_inicial()

if col2.button("Page 3"):
    pagina_sobre()

if col3.button("Page 4"):
    pagina_contato()

# 1.2 Darkmode function
def toggle_dark_mode():
    # Adiciona o botão ao lado do título
    button_clicked = st.button("🌙 Toggle Dark Mode")

    if button_clicked:
        st.session_state.dark_mode = not st.session_state.get("dark_mode", False)

    return st.session_state.get("dark_mode", False)

# Setting the button (dark/light)
dark_mode = toggle_dark_mode()
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

# 1.2.1 Skipping two lines
st.write(" ")
st.write(" ")

# 1.3 Database (collect and treatment)
df = pd.read_csv("data_for_dash.csv")

# 1.3.1 Transforming to date format
df['ACTIVITY_DATE'] = pd.to_datetime(df['ACTIVITY_DATE'])

# 1.3.2 Transforming to ascending date
def sort_df_by_activity_date(dataframe):
    return dataframe.sort_values(by='ACTIVITY_DATE')

# 1.3.3 Setting the filters in columns

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns (3)

# 1.3.3.1 "Start date" and "End Date"
with col1:
    date_group_option = st.radio("Date Grouping", ['7 days', '14 days', 'Lifetime'])

    if date_group_option == '7 days':
        start_date = st.date_input('Select Start Date', value=pd.to_datetime('today') - pd.DateOffset(days=7))
    elif date_group_option == '14 days':
        start_date = st.date_input('Select Start Date', value=pd.to_datetime('today') - pd.DateOffset(days=14))
    else:  # 'All'
        start_date = st.date_input('Select Start Date', value=df['ACTIVITY_DATE'].min())

with col3:
    end_date = st.date_input('Select End Date')

# 1.3.3.2 Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# 1.3.3.3 Filter dropdown campaign (BOX) - Filter: Media buyer and active within
with col2:
    media_buyer_filtered = st.selectbox("Select a media buyer", df['MEDIA_BUYER'].unique())
with col4:
    campaign_filtered = st.selectbox("Select a campaign", df['CAMPAIGN'].unique())
with col5:
    active_within_days = st.number_input('Active Within (Days)', min_value=1, max_value=15, value=15)

# 1.4 - Creating a new dataframe filtered to the graphs analysis
filtered_df = df[(df['ACTIVITY_DATE'] >= start_date) & (df['ACTIVITY_DATE'] <= end_date) &
                 (df['CAMPAIGN'] == campaign_filtered) & (df['MEDIA_BUYER'] == media_buyer_filtered)]

# 1.4.1 Function to sum the "DAILY_RETURN" per date
summed_df = filtered_df.groupby('ACTIVITY_DATE')['DAILY_RETURN'].sum().reset_index()


# 1.5 Creating all the graphics with plotly.express
daily_fig = px.line(filtered_df, x="ACTIVITY_DATE", y="DAILY_RETURN", title="DAILY RETURN", labels={'DAILY_RETURN': 'DAYLY_RETURN'})
st.plotly_chart(daily_fig, use_container_width=True)

total_return = px.line(filtered_df,x="ACTIVITY_DATE", y="TOTAL_RETURN",title="TOTAL RETURN", color="MEDIA_BUYER",labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(total_return, use_container_width=True)

daily_profit = px.line(filtered_df,x="ACTIVITY_DATE", y="DAILY_PROFIT",title="DAILY PROFIT", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(daily_profit, use_container_width=True)

total_profit = px.line(filtered_df,x="ACTIVITY_DATE", y="TOTAL_PROFIT",title="TOTAL PROFIT", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(total_profit, use_container_width=True)

spend_revenue = px.line(filtered_df,x="ACTIVITY_DATE", y="REVENUE",title="SPEND REVENUE", labels={'TOTAL_RETURN': 'TOTAL_RETURN'})
st.plotly_chart(spend_revenue, use_container_width=True)

# 1.5.1 columns for the next graphic
required_columns = ['SPEND_PER_ARRIVAL', 'REVENUE_PER_ARRIVAL', 'PROFIT_PER_ARRIVAL']
if all(column in filtered_df.columns for column in required_columns):
    # Crie um gráfico de linhas usando plotly express
    line_chart = px.line(filtered_df, x='ACTIVITY_DATE', y=required_columns, labels={'value': 'Value', 'variable': 'Metric'},
                         title=f"*SPEND PER ARRIVAL, REVENUE PER ARRIVAL AND PROFIT PER ARRIVAL - {media_buyer_filtered} - {campaign_filtered}")

    st.plotly_chart(line_chart, use_container_width=True)
else:
    st.warning(f"Columns {', '.join(required_columns)} not found in the filtered data.")



if 'ACCEPTANCE_RATE' in filtered_df.columns:
    # 1.5.2 Calculating the average ACCEPTANCE_RATE within the filtered period
    average_acceptance_rate = filtered_df['ACCEPTANCE_RATE'].mean()

    # 1.5.3 Showing the mean value in HTML
    st.markdown(f'<div style="width:100%; text-align:center; font-size:54px;">'
                f'Average Acceptance Rate: {average_acceptance_rate:.2%}</div>', unsafe_allow_html=True)

    # 1.5.4 Widget st.metric to show the mean value
    st.metric("Acceptance Rate (Average)", value=round(average_acceptance_rate, 4))
else:
    st.warning("Column 'ACCEPTANCE_RATE' not found in the filtered data.")


#Thanks for the opportunity
#Hope you like it.

