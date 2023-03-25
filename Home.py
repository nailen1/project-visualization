import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Auction items data dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

st.title(":house: 법원 부동산 경매 데이터")
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

date_min = min(df['casedate_full'].unique().tolist())
date_max = max(df['casedate_full'].unique().tolist())

st.subheader(
    f":chart_with_upwards_trend: 부동산 경매 시장 동향")
# st.text('')

# st.markdown("---")
with st.expander("요약 정보", expanded=True):
    st.metric('기간', f'{date_min} ~ {date_max}',
              delta_color="normal", help=None, label_visibility="visible")
    st.text('')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('전체 경매 물건 수', num_of_items+'개', "-3%",
                  delta_color="normal", help=None, label_visibility="visible")
    with col2:
        st.metric('경매 물건 감정가 총합', total_estimate+'원', "-8%",
                  delta_color="normal", help=None, label_visibility="visible")
    with col3:
        st.metric('평균 물건 입찰가 총합', total_bidding+'원', delta='-5%',
                  delta_color="normal", help=None, label_visibility="visible")
    with col4:
        st.metric('평균 유찰 횟수', mean_of_miss+'회', delta='0',
                  delta_color="normal", help=None, label_visibility="visible")
    st.text('')

list_address_sido = df['address_sido'].unique().tolist()
list_category = df['category'].unique().tolist()

st.sidebar.subheader("관심 범위 선택")

with st.sidebar.expander(f"관심 지역 선택 (전국 {len(list_address_sido)}개 시도)"):
    selected_sidos = st.multiselect(
        "", options=list_address_sido, default=list_address_sido)

with st.sidebar.expander(f"관심 카테고리 선택 (총 {len(list_category)}종)"):
    selected_cats = st.multiselect(
        "", options=list_category, default=['아파트', '다세대', '다가구주택', '연립주택', '단독주택'])

# colA, colB = st.columns(2)
# with colA:
#     with st.expander(f"관심 지역 선택 (전국 {len(list_address_sido)}개 시도)"):
#         selected_sidos = st.multiselect(
#             "", options=list_address_sido, default=list_address_sido)
# with colB:
#     with st.expander(f"관심 카테고리 선택 (총 {len(list_category)}종)"):
#         selected_cats = st.multiselect(
#             "", options=list_category, default=list_category)

df_selected_sido = df[df['address_sido'].isin(selected_sidos)]
df_selected_cat = df[df['category'].isin(selected_cats)]

st.subheader(f":bar_chart: 관심 지역 기준 물건 수")

with st.expander(f"선택 지역: {len(selected_sidos)}개, 선택 카테고리: {len(selected_cats)}개", expanded=True):
    # st.info(f"지역별 법원경매 부동산 물건 수 ('23.3.26~)")
    df_sido_total = df_selected_sido.groupby(
        'address_sido').size().reset_index(name="number")
    df_sido_cat = df_selected_sido[df_selected_sido['category'].isin(selected_cats)].groupby(
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

    fig1.update_xaxes(title_text='지역 이름')
    fig1.update_yaxes(title_text='물건 수')

    # fig1.update_layout(template='xgridoff')

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

    fig1.add_hline(y=df_sido_total['number'].mean(), line_width=1,
                   line_color="gray",
                   annotation_text="전국 평균",  # 주석
                   annotation_position="top right",
                   annotation_font_size=10)

    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)

st.subheader(f":bar_chart: 관심 카테고리 기준 물건 수")

with st.expander(f"선택 지역: {len(selected_sidos)}개, 선택 카테고리: {len(selected_cats)}개", expanded=True):

    df_cat_total = df_selected_cat.groupby(
        'category').size().reset_index(name="number")
    df_cat_sido = df_selected_cat[df_selected_cat['address_sido'].isin(selected_sidos)].groupby(
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

    fig2.update_xaxes(title_text='카테고리')
    fig2.update_yaxes(title_text='물건 수')

    # fig2.update_layout(template='ggplot2')

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

    fig2.add_hline(y=df_cat_total['number'].mean(), line_width=1,
                   line_color="gray",
                   annotation_text="카테고리 평균",  # 주석
                   annotation_position="top right",
                   annotation_font_size=10)

    st.plotly_chart(fig2, theme='streamlit', use_container_width=True)

st.text('')
st.subheader(':bar_chart: 날짜별 물건 수')

with st.expander(f"5일 이동 평균선", expanded=True):
    df_date_line = df.groupby(
        'casedate_full').size().reset_index(name="number")
    df_date_line['date'] = pd.to_datetime(df_date_line['casedate_full'])

    fig3 = px.scatter(df_date_line, x="date", y="number", trendline="rolling",
                      trendline_options=dict(window=5))
    fig3.update_layout(xaxis=dict(rangeslider_visible=True))

    st.plotly_chart(fig3, theme='streamlit', use_container_width=True)
