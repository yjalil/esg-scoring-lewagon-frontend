import streamlit as st
import requests
import json
import pandas as pd
from config import BASE_URI

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
    st.dataframe(df)
    