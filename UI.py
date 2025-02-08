import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from data_util import get_cat_df

@st.dialog("Add New Expense")
def _new_expense():
    st.write("Enter Expense")

    date = st.date_input("Select date")
    reason = st.text_input("Enter Reason")
    category = st.selectbox("Select Category",("Food", "Drink", "Flat","Other"))
    amount = st.number_input("Enter Amount")

    if st.button("Add Expense"):
        st.session_state['df_result'].loc[len(st.session_state['df_result'])] = {"date":str(date),"reason":str(reason),"category":str(category),"amount":int(amount)}
        new_df = st.session_state['df_result']
        new_df.to_json('data.json')
        st.session_state['df_grp'] = get_cat_df(new_df)
        st.rerun()


if "df_result" not in st.session_state:
    st.session_state['df_result'] = pd.DataFrame(columns=['date','reason','category','price'])

if "df_grp" not in st.session_state:
    st.session_state['df_grp'] = pd.DataFrame(columns=['category','amount'])


if os.path.isfile('data.json')==False:
    data = {"date": [],"reason":[],"category":[],"amount":[]}
    with open('data.json','w+') as f:
        json.dump(data, f)
    st.session_state['df_result'] = pd.DataFrame(data)


if os.path.isfile('data.json')==True:
    with open('data.json') as json_file:
        print("loaded")
        try:
            data = json.load(json_file)
        except Exception:
            data = {"date": [],"reason":[],"category":[],"amount":[]}
        st.session_state['df_result'] = pd.DataFrame(data)


columns = st.columns((1,1))
with columns[0]:
    if st.button('Add New Expense'):
        _new_expense()

with columns[1]:
    if st.button('CLEAR !!'):
        data = {"date": [],"reason":[],"category":[],"amount":[]}
        with open('data.json','w+') as f:
            json.dump(data, f)
        st.session_state['df_result'] = pd.DataFrame(data)
        st.session_state['df_grp'] = pd.DataFrame({"category":[],"amount":[]})


df = st.session_state['df_result']
cat_grp = get_cat_df(df)



container = st.container(border=True)
container.header("TOTAL : :blue["+str(sum(st.session_state['df_result']['amount']))+"]")

tabs = st.tabs(['Data','Graph'])

with tabs[0]:
    st.dataframe(st.session_state['df_result'], use_container_width=True)

with tabs[1]:
    st.dataframe(st.session_state['df_grp'], use_container_width=True)

    st.subheader("Amount per Category")
    fig = px.bar(st.session_state['df_grp'], x='category', y='amount',text_auto=True)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

    st.subheader("Amount per Category")
    fig_donut = px.pie(st.session_state['df_grp'], values='amount', names='category', hole=0.4)
    st.plotly_chart(fig_donut)

    st.subheader("Amount per Day")
    fig = px.bar(st.session_state['df_result'], x='date', y='amount',color='category',text_auto=True)
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)
