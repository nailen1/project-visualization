import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title(":house: 카테고리 기준 물건 살펴보기")
st.text('')

df = pd.read_csv('./database/auction-items-nonan.csv')

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

df_selected = df[df['category'].isin(selected_cats)]

st.info(f"카테고리별 법원경매 부동산 물건 수 ('23.3.26~)")

with st.expander(f"선택 지역: {len(selected_sidos)}개, 선택 카테고리: {len(selected_cats)}개", expanded=True):
    df_cat_total = df_selected.groupby(
        'category').size().reset_index(name="number")
    df_cat_sido = df_selected[df_selected['address_sido'].isin(selected_sidos)].groupby(
        'category').size().reset_index(name="number")

    list_cat = df_cat_total['category'].unique().tolist()

    y21 = df_cat_total['number'].values.tolist()
    y22 = df_cat_sido['number'].values.tolist()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="전체", x=list_cat, y=y21, text=y21))
    fig2.add_trace(go.Bar(
        name=f"선택된 지역 {selected_sidos[:3]} 등 {len(selected_sidos)}곳", x=list_cat, y=y22, text=y22))

    fig2.update_traces(textfont_size=12, textangle=90,
                       textposition="outside", cliponaxis=False)

    fig2.update_traces(marker_line_width=0.5, opacity=1)

    fig2.update_xaxes(title_text='지역 이름)')
    fig2.update_yaxes(title_text='물건 수')

    fig2.update_layout(template='xgridoff')

    fig2.update_layout(legend_orientation="h",
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

    st.plotly_chart(fig2, theme='streamlit', use_container_width=True)
