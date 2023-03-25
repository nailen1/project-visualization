import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title(":house: 관심 평균값 살펴보기")

df = pd.read_csv('./database/auction-items-nonan.csv')

list_var_kr = ['감정가', '최저입찰가', '유찰횟수', '면적']
dict_var = {'감정가': 'price_estimate', '최저입찰가': 'price_bidding',
            '유찰횟수': 'number_miss', '면적': 'area'}
list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
list_cat = ['모든 종류'] + df['category'].unique().tolist()

selected_key = st.selectbox('관심 변수 선택', list_var_kr)

st.subheader(f":chart_with_upwards_trend: 지역별 {selected_key} 평균치")
st.text('')

selected_cat = st.selectbox('카테고리 선택', list_cat)

means_sido = []
df_cat = df[df['category'] == selected_cat]
if selected_cat == '모든 종류':
    df_cat = df
for sido in list_sido:
    if sido == '전체 지역':
        mean = df[dict_var[selected_key]].mean()
    else:
        mean = df_cat[df_cat['address_sido'] ==
                      sido][dict_var[selected_key]].mean()
    means_sido.append(mean)

fig1 = go.Figure()

fig1.add_trace(go.Bar(name="전체", x=list_sido, y=means_sido))

with st.expander(f"선택 카테고리: {selected_cat}", expanded=True):
    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)

st.subheader(f":chart_with_upwards_trend: 카테고리별 {selected_key} 평균치")
st.text('')

selected_sido = st.selectbox('지역(시도) 선택', list_sido)

means_cat = []
df_sido = df[df['address_sido'] == selected_sido]
if selected_cat == '모든 종류':
    df_sido = df
for cat in list_cat:
    if cat == '모든 종류':
        mean = df[dict_var[selected_key]].mean()
    else:
        mean = df_sido[df_sido['category'] ==
                       cat][dict_var[selected_key]].mean()
    means_cat.append(mean)

fig2 = go.Figure()

fig2.add_trace(go.Bar(name="전체", x=list_cat, y=means_cat))

with st.expander(f"선택 지역: {selected_sido}", expanded=True):
    st.plotly_chart(fig2, theme='streamlit', use_container_width=True)