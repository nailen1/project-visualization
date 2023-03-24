import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

st.header('감정가 별 물건 수')

address_sido = st.selectbox('지역 선택(시도)', list_sido)
selected_region = address_sido

price_start = 0
price_end = 1000000000
price_step = 1000000
price_range = st.slider("가격 범위 지정", 0, 1000000000,
                        (price_start, price_end), price_step)

df = pd.read_csv('./database/auction-items-nonan.csv')

df_price = df[df['price_estimate'] <= price_range[1]
              ][df['price_estimate'] >= price_range[0]]

if address_sido != '전체 지역':
    df_price = df_price[df_price['address_sido'] == address_sido]

price_min = price_range[0]
price_max = price_range[1]


def convertPrice(price):
    if price == 0:
        return price
    if price >= 1000000 and price < 10000000:
        price = str(round(price/1000000, 1))+'백만'
        return price
    if price >= 10000000 and price < 100000000:
        price = str(round(price/10000000, 1))+'천만'
        return price
    if price > 100000000:
        price = str(round(price/100000000, 1))+'억'
        return price


st.text(
    f"가격 선택 범위: {convertPrice(price_min)}원부터 {convertPrice(price_max)}원까지")

# df_price = df[df['price_estimate'] <= price_range[1] | df['price_estimate'] >= price_range[0]]

df_bin_estimate = df_price.groupby(
    pd.cut(df_price['price_estimate'], bins=20)).size().reset_index(name='number')
df_bin_estimate = df_bin_estimate.reset_index()
df_bin_estimate['index'] = df_bin_estimate['index']+1

fig = px.bar(df_bin_estimate, x='index', y='number', text='number')

st.bar_chart(data=df_bin_estimate, x='index', y='number',
             width=0, height=0, use_container_width=True)

st.plotly_chart(fig, theme=None, use_container_width=True)
