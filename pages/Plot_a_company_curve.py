import streamlit as st
import requests
import json
import pandas as pd
from config import BASE_URI


def map_topic_weight(text):
    if text == 'Social':
        return 0.31
    if text == 'Environmental':
        return 0.44
    if text == 'Governance':
        return 0.25
    else:
        return 0.0
    
st.set_page_config(page_title="Plotting Company ESG trend", page_icon="📈")


tuple_companies = []
response = requests.get(f"{BASE_URI}/companies/").json()
for JSONcompany in response :
    tuple_companies.append(JSONcompany['name']) 

st.markdown("# Company Plot")
st.sidebar.header("Company Plot")
st.write(
    """You can pick a company from the dropdown menu from all available Moroccan companies in our database. Pick a start and end date for a period to plot."""
)



start_date = st.date_input('Start date')
end_date = st.date_input('End date')
company = st.selectbox(
    'Company',
    tuple(tuple_companies))

if st.button('Plot'):
    response_plot = requests.get(f"{BASE_URI}/articles/byCompany/{company}/Period/{start_date}/{end_date}")
    df = pd.DataFrame(response_plot.json())
    # st.write(df['date'].dtype)
    df['weights'] = df['topic_category'].apply(map_topic_weight)
    df['esg_agg_score'] = df['weights'] * df['esg_score']
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.sort_values(by='date', ascending=True, inplace=True)
    df['cumul'] = df['esg_score'].cumsum()
    # st.dataframe(df)
    st.line_chart(data=df, x = 'date', y= 'cumul' )
