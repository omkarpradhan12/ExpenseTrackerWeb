import pandas as pd

def get_cat_df(df):
    cat_grp = df[['paid_by','amount']].groupby(by='paid_by').sum().reset_index()
    return cat_grp

