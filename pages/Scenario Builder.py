import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
st.title("Build out your Villian and Encounters")


def get_by_typecode(type_code):
    df = pd.read_parquet('cards.parquet')
    df2 = df[df['type_code'].isin([type_code])]
    return df2

def get_by_factioncode(faction_code):
    df = pd.read_parquet('cards.parquet')
    df2 = df[df['faction_code'].isin([faction_code])]
    return df2

def count_by_type(df):
    df2 = df[['type_code']].groupby(['type_code']).size()\
        .reset_index(name='counts')
    return df2 

def df_select(df):
    df2 = df.copy()
    df2.insert(0, "select", False)

    df_sel = st.data_editor(
        df2,
        hide_index=True,
        column_config={
            "select": st.column_config.CheckboxColumn(required=True)
        },
        disabled=df.columns,
    )

    sel_sets = df_sel[df_sel.select]
    return sel_sets.drop('select', axis=1)

col1, col2 = st.columns(2)

with col1:
    faction_code = 'encounter'
    enc = get_by_factioncode(faction_code)
    df = enc[enc['type_code'] != 'villain']
    df = df[['set_code']].drop_duplicates()
    sel = df_select(df=df)
    st.write(sel)

with col2:
    type_ct = count_by_type(enc)
    st.subheader("Count by Card Type")
    st.bar_chart(data=type_ct, x='type_code', y='counts')

    set_fil = [i for i in sel['set_code'].values]
    df = get_by_factioncode('encounter')
    df2 = df[df['set_code'].isin(set_fil)]
    type_ct2 = count_by_type(df2)
    st.subheader("Filtered")
    st.bar_chart(type_ct2, x='type_code', y='counts')
    st.write(set_fil)
