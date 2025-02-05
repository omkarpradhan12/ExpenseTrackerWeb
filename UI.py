import streamlit as st
import pandas as pd
import json
import os

if "df_result" not in st.session_state:
    st.session_state['df_result'] = pd.DataFrame(columns=['date','reason','category','price'])


if os.path.isfile('data.json')==False:
    data = {"date": [],"reason":[],"category":[],"price":[]}
    with open('data.json','w+') as f:
        json.dump(data, f)
    st.session_state['df_result'] = pd.DataFrame(data)


if os.path.isfile('data.json')==True:
    with open('data.json') as json_file:
        print("loaded")
        data = json.load(json_file)
        st.session_state['df_result'] = pd.DataFrame(data)



st.write("Inside the form")

date = st.date_input("Select date")
reason = st.text_input("Enter Reason")
category = st.selectbox("Select Category",("Food", "Drink", "Flat","Other"))
price = st.number_input("Enter Price")




if st.button('Add Expense'):

    # print("date", date, "reason", reason, "category", category, "price", price)
    # # pd.concat(dataframe,pd.DataFrame())
    st.session_state['df_result'].loc[len(st.session_state['df_result'])] = {"date":str(date),"reason":str(reason),"category":str(category),"price":str(price)}
    new_df = st.session_state['df_result']
    new_df.to_json('data.json')


if st.button('CLEAR !!'):
    data = {"date": [],"reason":[],"category":[],"price":[]}
    with open('data.json','w+') as f:
        json.dump(data, f)
    st.session_state['df_result'] = pd.DataFrame(data)



st.dataframe(st.session_state['df_result'])
