import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title(":house: 지역 기준 물건 살펴보기")
st.text('')

df = pd.read_csv('./database/auction-items-nonan.csv')

num_of_items = str(df.shape[0])
mean_of_miss = str(round(df['number_miss'].mean(), 1))


def convertPrice(price):
    if price == 0:
        return price
    if price >= 1000000 and price < 10000000:
        price = str(round(price/1000000, 1))+'백만'
        return price
    if price >= 10000000 and price < 100000000:
        price = str(round(price/10000000, 1))+'천만'
        return price
    if price > 100000000 and price < 1000000000000:
        price = str(round(price/100000000, 1))+'억'
    if price > 1000000000000 and price < 10000000000000000:
        price = str(round(price/1000000000000, 1))+'조'
        return price


total_estimate = convertPrice(df['price_estimate'].sum())
total_bidding = convertPrice(df['price_bidding'].sum())

list_address_sido = df['address_sido'].unique().tolist()
list_category = df['category'].unique().tolist()

colA, colB = st.columns(2)
with colA:
    with st.expander(f"관심 지역 선택 (전국 {len(list_address_sido)}개 시도)"):
        selected_sidos = st.multiselect(
            "", options=list_address_sido, default=list_address_sido)

with colB:
    with st.expander(f"관심 카테고리 선택 (총 {len(list_category)}종)"):
        selected_cats = st.multiselect(
            "", options=list_category, default=list_category)

df_selected = df[df['address_sido'].isin(selected_sidos)]

st.info(f"지역별 법원경매 부동산 물건 수 ('23.3.26~)")

with st.expander(f"선택 지역: {len(selected_sidos)}개, 선택 카테고리: {len(selected_cats)}개", expanded=True):
    # st.info(f"지역별 법원경매 부동산 물건 수 ('23.3.26~)")
    df_sido_total = df_selected.groupby(
        'address_sido').size().reset_index(name="number")
    df_sido_cat = df_selected[df_selected['category'].isin(selected_cats)].groupby(
        'address_sido').size().reset_index(name="number")

    list_sido = df_sido_total['address_sido'].unique().tolist()

    y11 = df_sido_total['number'].values.tolist()
    y12 = df_sido_cat['number'].values.tolist()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="전체", x=list_sido, y=y11, text=y11))
    fig1.add_trace(go.Bar(
        name=f"선택된 카테고리 {selected_cats[:3]} 등 {len(selected_cats)}종", x=list_sido, y=y12, text=y12))

    fig1.update_traces(textfont_size=12, textangle=90,
                       textposition="outside", cliponaxis=False)

    fig1.update_traces(marker_line_width=0.5, opacity=1)

    fig1.update_xaxes(title_text='지역 이름)')
    fig1.update_yaxes(title_text='물건 수')

    fig1.update_layout(template='xgridoff')

    fig1.update_layout(legend_orientation="h",
                       legend_valign="top",
                       legend_x=0,
                       legend_y=1.2,
                       #   legend_borderwidth=1,
                       #   legend_bordercolor='#000',
                       legend_entrywidthmode='fraction',
                       legend_entrywidth=1,
                       # legend_title_font_family = "Times New Roman",
                       # legend_title_font_color="red",
                       # legend_title_font_size= 20,
                       # legend_font_family="Courier",
                       # legend_font_size=12,
                       # legend_font_color="black",
                       # legend_bgcolor="LightSteelBlue",
                       # legend_bordercolor="Black",
                       )

    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)
