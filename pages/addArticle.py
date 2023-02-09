import streamlit as st
import requests
import numpy as np
import pandas as pd
from config import BASE_URI


st.set_page_config(
    page_title="Add an article",
    page_icon="👋",
)

st.write("# Test our models on a single article")

st.markdown(
    """
    For model testing only the article body text is needed. If the user is satisfied with the ouptut the article can be added to the database. 
    An article must have the following fields not empty :
    * Title
    * Date
    * Source
    * Body
"""
)

body = st.text_area('Text to analyze', '''Your text here''')
response = requests.post(f"{BASE_URI}/article/predict/",json={'body':body})

st.markdown("""--------------------------------------------------------------""")
try :
    st.write('Category:', response.json()['topic_category'])
except :
    st.write('Category : Nothing to score yet')

try: 
    st.write('Sentiment score:', response.json()['esg_score'])
except:
    st.write('Sentiment score : Nothing to score yet')



st.markdown("""--------------------------------------------------------------""")

title = st.text_input('Article title')
date = st.text_input('Article date')
company = st.text_input('Company name')
source = st.text_input('Article source')

if st.button('Send to database'):
    process_date = np.datetime64('now')
    company_response_get = requests.get(f"{BASE_URI}/companies/{company}")
    if company_response_get.status_code == 404:
        company_response = requests.post("{BASE_URI}/company/add/",json={'name':company,
                                                                                'description':'No description provided'})

    model_response = requests.post(f"{BASE_URI}/article/predict/",json={'body':body})
    response = requests.post(f"{BASE_URI}/article/add/{company}",json={
        "date": date,
        "title": title,
        "uploaded_at": pd.to_datetime(str(process_date)).strftime('%Y-%m-%d'),
        "body": body,
        "sourceURL": source,
        "topic_category": model_response.json()['topic_category'],
        "esg_score": model_response.json()['esg_score'],
        "scored_at": pd.to_datetime(str(process_date)).strftime('%Y-%m-%d'),
        "exclude_count": 0
    })
