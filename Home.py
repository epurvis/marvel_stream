import streamlit as st
import pandas as pd
st.set_page_config(layout='wide')

st.title('Marvel Champions DB')

col1, col2 = st.columns(2)

def load_heroes():
    df = pd.read_parquet('cards_img_fix.parquet')
    df_heroes = df[(df.type_code == 'hero')]
    df_heroes['name'] = df['name'] + ' ' + df['code'].str[4:]
    df_return = df_heroes[['code','name', 'traits', 'attack', 'thwart', 'defense', 'hand_size', 'image_url']]
    return df_return

with col1:
    st.dataframe(load_heroes(), column_config={
        'image_url': st.column_config.ImageColumn(
            'Card Preview'
        )
    })

with col2:
    st.bar_chart(load_heroes(), x='name', y=['attack','thwart','defense'])
    st.bar_chart(load_heroes(), x='name', y='hand_size')



