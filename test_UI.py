import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from data_util import get_cat_df

def load_data():
    if os.path.isfile('data.json'):
        with open('data.json') as f:
            try:
                return pd.DataFrame(json.load(f))
            except json.JSONDecodeError:
                return pd.DataFrame(columns=['date', 'reason', 'paid_by', 'amount'])
    else:
        return pd.DataFrame(columns=['date', 'reason', 'paid_by', 'amount'])

def save_data(df):
    df.to_json('data.json')

@st.dialog("Add New Expense")
def _new_expense():
    st.write("Enter Expense")
    date = st.date_input("Select date")
    reason = st.text_input("Enter Reason")
    paid_by = st.selectbox("Paid By",("Omkar","Shashank","Sarvadnya","Ankita","Aniket","Kshama","Sachi","JP"))
    amount = st.number_input("Enter Amount")
    if st.button("Add Expense"):
        new_row = pd.DataFrame([{"date": str(date), "reason": str(reason), "paid_by": paid_by.capitalize(), "amount": int(amount)}])
        st.session_state['df_result'] = pd.concat([st.session_state['df_result'], new_row], ignore_index=True)
        save_data(st.session_state['df_result'])
        st.session_state['df_grp'] = get_cat_df(st.session_state['df_result'])
        st.rerun()

@st.dialog("Edit Expense")
def _edit_expense(index_to_edit):
    st.write("Edit Expense")
    expense_to_edit = st.session_state['df_result'].iloc[index_to_edit].to_dict()
    date = st.date_input("Select date", value=pd.to_datetime(expense_to_edit['date']).date())
    reason = st.text_input("Enter Reason", value=expense_to_edit['reason'])
    paid_by = st.selectbox("Paid By", ("Omkar", "Shashank", "Sarvadnya", "Ankita", "Aniket", "Kshama", "Sachi", "JP"), index=("Omkar", "Shashank", "Sarvadnya", "Ankita", "Aniket", "Kshama", "Sachi", "JP").index(expense_to_edit['paid_by']))
    amount = st.number_input("Enter Amount", value=int(expense_to_edit['amount']))
    if st.button("Save Changes"):
        st.session_state['df_result'].loc[index_to_edit] = {"date": str(date), "reason": str(reason), "paid_by": paid_by.capitalize(), "amount": int(amount)}
        save_data(st.session_state['df_result'])
        st.session_state['df_grp'] = get_cat_df(st.session_state['df_result'])
        st.rerun()

if 'df_result' not in st.session_state:
    st.session_state['df_result'] = load_data()

if 'df_grp' not in st.session_state:
    st.session_state['df_grp'] = get_cat_df(st.session_state['df_result'])

columns = st.columns((1, 1))
with columns[0]:
    if st.button('Add New Expense'):
        _new_expense()

with columns[1]:
    if st.button('CLEAR !!'):
        st.session_state['df_result'] = pd.DataFrame(columns=['date', 'reason', 'paid_by', 'amount'])
        save_data(st.session_state['df_result'])
        st.session_state['df_grp'] = pd.DataFrame({"paid_by": [], "amount": []})
        st.rerun()

st.header("Expenses")
df = st.session_state['df_result'].copy()

if not df.empty:
    df['Select'] = False  # Add a boolean column for selection
    edited_df = st.data_editor(df, column_config={
        "Select": st.column_config.CheckboxColumn(
            "Select",
            default=False,
        )
    }, num_rows="dynamic")

    selected_indices_to_delete = edited_df[edited_df['Select']].index.tolist()

    col_buttons = st.columns(2)
    with col_buttons[0]:
        if st.button("Delete Selected"):
            if selected_indices_to_delete:
                st.session_state['df_result'] = st.session_state['df_result'].drop(selected_indices_to_delete).reset_index(drop=True)
                save_data(st.session_state['df_result'])
                st.session_state['df_grp'] = get_cat_df(st.session_state['df_result'])
                st.rerun()
            else:
                st.warning("No rows selected for deletion.")

    with col_buttons[1]:
        if st.button("Edit Selected"):
            if len(edited_df[edited_df['Select']]) == 1:
                index_to_edit = edited_df[edited_df['Select']].index[0]
                _edit_expense(index_to_edit)
            elif len(edited_df[edited_df['Select']]) > 1:
                st.warning("Please select only one row to edit.")
            else:
                st.info("Select a row to edit.")

else:
    st.info("No expenses recorded yet. Click 'Add New Expense' to start.")

container = st.container(border=True)
container.header(f"TOTAL : :blue[{df['amount'].sum() if not df.empty else 0}]")

tabs = st.tabs(['Data', 'Graph'])

with tabs[0]:
    st.subheader("Per Head Payment Data")
    if not st.session_state['df_result'].empty:
        st.dataframe(st.session_state['df_grp'], use_container_width=True)
    else:
        st.info("No expense data to display.")

with tabs[1]:
    if not st.session_state['df_grp'].empty:
        st.subheader("Amount per Person")
        fig_bar = px.bar(st.session_state['df_grp'], x='paid_by', y='amount', text_auto=True)
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar)

        st.subheader("Amount per Person (Donut)")
        fig_donut = px.pie(st.session_state['df_grp'], values='amount', names='paid_by', hole=0.4)
        st.plotly_chart(fig_donut)

    else:
        st.info("No data to display in graphs yet.")
