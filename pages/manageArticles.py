import streamlit as st
import requests
import json
import pandas as pd
from config import BASE_URI


st.set_page_config(page_title="Cleaning database", page_icon="📈")
# st.write({BASE_URI})

tuple_companies = []
response = requests.get(f"{BASE_URI}/companies/").json()
for JSONcompany in response :
    tuple_companies.append(JSONcompany['name']) 

st.markdown("# Company Articles")
st.sidebar.header("Company Articles")
st.write(
    """You can delete articles that might seem problematic"""
)

start_date = st.date_input('Start date')
end_date = st.date_input('End date')
company = st.selectbox(
    'Company',
    tuple(tuple_companies))

if st.button('Show Articles'):
                            #   {BASE_URI}/articles/byCompany/detailed/Tesla/Period/2010-01-01/2023-02-08
    response = requests.get(f"{BASE_URI}/articles/byCompany/detailed/{company}/Period/{start_date}/{end_date}")
    
    for article in response.json():
        with st.expander(label = f"{article['id']} : {article['date']} | {article['title']})"):
            st.markdown(f"[Read more]({article['sourceURL']})")
            st.metric(label="Topic", value=article['topic_category'])
            st.metric(label="Sentiment", value=article['esg_score'])
            # if st.button(label="Delete Article", key = f"Delete Article {article['id']}"):
            #     requests.delete(f"{BASE_URI}/article/delete/{article['id']}")
            if st.button(label="Flag for Retraining", key = f"Flag for Retraining {article['id']}"):
                requests.patch(f"{BASE_URI}/article/flag/{article['id']}")
