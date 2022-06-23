import streamlit as st
import pandas as pd
import requests
import altair as alt

st.title("ETF Composition")

df = pd.read_csv('data/fund_compositions.csv')

choice = st.selectbox("Select a fund", df.Fund.unique())

selected_fund = df[df.Fund == choice].drop(columns=['Fund']).copy()
sectors = selected_fund.groupby('Sector')['Weight (%)'].sum()
regions = selected_fund.groupby('Location')['Weight (%)'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Top 10 concentration", value=f"{selected_fund.iloc[:10]['Weight (%)'].sum():.0f}%")
col2.metric("Largest sector", value=f'{sectors.max():.0f}%', delta=sectors.idxmax(), delta_color='off')
col3.metric("Largest region", value=f'{regions.max():.0f}%', delta=regions.idxmax(), delta_color='off')

st.header('Sectors')
c = alt.Chart(sectors.reset_index()).mark_bar().encode(
    x='Weight (%)',
    y='Sector'
)
st.altair_chart(c, use_container_width=True)

st.header('Holdings')
st.dataframe(selected_fund)