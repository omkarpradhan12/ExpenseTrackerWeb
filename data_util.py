import pandas as pd

def get_cat_df(df):
    cat_grp = df[['category','amount']].groupby(by='category').sum().reset_index()
    return cat_grp

