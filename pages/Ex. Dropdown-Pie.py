import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# df = pd.read_csv('../dataset-auction-items/auction-items-total.csv')
# df_seoul = df[df['address_sido'] == '서울특별시']

# df_bar = pd.DataFrame({'Category': df_seoul['category'].value_counts(
# ).index, "Number": df_seoul['category'].value_counts().values})

# st.write('부동산 종류별 물건 수: 서울특별시')

# st.bar_chart(data=df_bar, x='Category', y='Number',
#              width=0, height=0, use_container_width=True)

list_sido = [
    '전체 지역',
    '서울특별시',
    '부산광역시',
    '대구광역시',
    '인천광역시',
    '광주광역시',
    '대전광역시',
    '울산광역시',
    '세종특별자치시',
    '경기도',
    '강원도',
    '충청북도',
    '충청남도',
    '전라북도',
    '전라남도',
    '경상북도',
    '경상남도',
    '제주특별자치도']

st.header('물건 별 비율')

address_sido = st.selectbox('지역 선택(시도)', list_sido)
selected_region = address_sido

df = pd.read_csv('./database/auction-items-nonan.csv')

if address_sido != '전체 지역':
    df = df[df['address_sido'] == address_sido]

fig = px.pie(df, names="category")

st.plotly_chart(fig, theme=None, use_container_width=True)
