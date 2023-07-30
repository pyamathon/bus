import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import plotly.graph_objects as go

# ページのタイトル設定
st.set_page_config(
    page_title = "bus",
    layout="wide"
)

# csv読み込み
df0 = pd.read_csv('bus.csv', index_col = 0, encoding="Shift-JIS")

# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = -1
    st.session_state.df0 = df0

# 各種メニューの非表示設定
hide_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html = True)

#選択する各項目のリスト作成用
def df_list(column):
    unique_list = st.session_state.df0[column].dropna(how='all').unique()
    st.session_state.df_list = unique_list

#選択されている項目のテキスト表示用
def add_text(selector, column):
    unique_list = st.session_state.df0[column].dropna(how='all').unique()
    sort_unique_list = np.sort(unique_list)
    selector = np.sort(selector)
    if np.array_equal(selector, sort_unique_list) == True:
        st.sidebar.text("全ての人が選ばれています。")
    else:
        st.sidebar.text(str(sort_unique_list).replace(str(selector),'') + "の人が除かれています。")

#サイドバーの時台→時間の変更判定
def change_around_time():
    start_6 = [s for s in st.session_state["time"] if s.startswith('6')]
    start_7 = [s for s in st.session_state["time"] if s.startswith('7')]
    start_8 = [s for s in st.session_state["time"] if s.startswith('8')]
    flag_list = [len(start_6), len(start_7), len(start_8)]
    original_list = [6, 7, 8]
    if (0 in flag_list) == True or len(st.session_state["around_time"]) != 3:
        judge_list = [s for s, x in enumerate(flag_list) if x != 0]
        new_list = []
        for i in range(len(judge_list)):
            new_list.append(original_list[judge_list[i]])
        st.session_state["around_time"] = new_list

def change_time():
    new_list =[]
    for i in range(len(st.session_state["around_time"])):
        new_list.extend([s for s in st.session_state.df0["始発時分"] if s.startswith(str(st.session_state["around_time"][i]))])
    st.session_state["time"] = new_list

# 最初のページ
def main_page():

    column_list = st.session_state.df0.columns[3:].values
    #column_list_selector = st.sidebar.multiselect("停留所", column_list, default = column_list)
    index_selector = st.sidebar.multiselect("出発時間", st.session_state.df0["始発時分"], default = st.session_state.df0["始発時分"], key = "time", on_change = change_around_time)

    #サイドバー作成用
    #[6,7,8]時台
    df_list('時代')
    around_time_selector = st.sidebar.multiselect("時台",st.session_state.df_list, default = st.session_state.df_list, key = "around_time", on_change = change_time)
    if len(around_time_selector) == 0:
        st.sidebar.text("どの時間も選ばれていません")
    elif len(around_time_selector) == 3:
        st.sidebar.text("全ての時台が選ばれています。")
    else:
        st.sidebar.text(''.join(str(around_time_selector)) + "時台が選ばれています。")

    #終点
    df_list("終点")
    end_point_selector = st.sidebar.multiselect("終点", st.session_state.df_list, default = st.session_state.df_list)
    if len(end_point_selector) == 0:
        st.sidebar.text("どの終点も選ばれていません")
    elif len(end_point_selector) == 2:
        st.sidebar.text("全ての終点が選ばれています。")
    else:
        st.sidebar.text(''.join(str(end_point_selector)) + "が選ばれています。")


    st.session_state.select_arr = st.session_state.df0[
                                        (
                                        st.session_state.df0["時代"].isin(around_time_selector)
                                        & st.session_state.df0["終点"].isin(end_point_selector)
                                        & st.session_state.df0["始発時分"].isin(index_selector)
                                        )
                                    ][column_list]

    st.session_state.select_arr1 = st.session_state.df0[
                                        (
                                        st.session_state.df0["時代"].isin(around_time_selector)
                                        & st.session_state.df0["終点"].isin(end_point_selector)
                                        & st.session_state.df0["始発時分"].isin(index_selector)
                                        )
                                    ]

    st.write(st.session_state.select_arr1)
    fig = go.Figure()
    for i in range(len(st.session_state.select_arr.index)):
        fig.add_traces(go.Scatter(x = st.session_state.select_arr.columns.values,
                          y = st.session_state.select_arr.T[st.session_state.select_arr.index[i]],
                          name = index_selector[i])
                )
    st.plotly_chart(fig)

# ページ判定
if st.session_state.page_id == -1:
    main_page()
