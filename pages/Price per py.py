import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title(":house: 평당 가격 살펴보기")

df = pd.read_csv('./database/auction-items-nonan.csv')

list_var_kr = ['감정가', '최저입찰가']
dict_var = {'감정가': 'price_estimate', '최저입찰가': 'price_bidding'}
list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
list_cat = ['모든 종류'] + df['category'].unique().tolist()

selected_key = st.selectbox('관심 변수 선택', list_var_kr)

st.subheader(
    f":chart_with_upwards_trend: 지역별 평당 {selected_key}")
st.text('')

selected_cat = st.selectbox('카테고리 선택', list_cat)

df_cat = df[df['category'] == selected_cat]
if selected_cat == '모든 종류':
    df_cat = df

prices_py = []
for sido in list_sido:
    df_sido = df_cat[df_cat['address_sido'] == sido]
    if sido == '전체 지역':
        df_sido = df_cat
    price_py = int(df_sido[dict_var[selected_key]
                           ].mean()/df_sido['area'].mean())
    prices_py.append(price_py)

fig1 = go.Figure()
fig1.add_trace(go.Bar(name="전체", x=list_sido, y=prices_py))

with st.expander(f"선택 카테고리: {selected_cat}", expanded=True):
    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)


st.subheader(
    f":chart_with_upwards_trend: 카테고리별 평당 {selected_key}")
st.text('')

selected_sido = st.selectbox('지역 선택', list_sido)


df_sido = df[df['address_sido'] == selected_sido]
if selected_sido == '모든 종류':
    df_sido = df

prices_py = []
for sido in list_sido:
    df_sido = df_cat[df_cat['address_sido'] == sido]
    if sido == '전체 지역':
        df_sido = df_cat
    price_py = int(df_sido[dict_var[selected_key]
                           ].mean()/df_sido['area'].mean())
    prices_py.append(price_py)

fig = go.Figure()
fig.add_trace(go.Bar(name="전체", x=list_sido, y=prices_py))

with st.expander(f"선택 카테고리: {selected_cat}", expanded=True):
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
