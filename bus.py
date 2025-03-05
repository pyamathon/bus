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
df1 = pd.read_csv('bus.csv', index_col = 0)
df2 = pd.read_csv('bus2.csv', index_col = 0)

# セッション情報の初期化
if "page_id" not in st.session_state:
    st.session_state.page_id = -1
    st.session_state.df1 = df1
    st.session_state.df2 = df2
    st.session_state.flag = 0


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
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
               .sidebar-content{
                    margin-top: -75px;
               }
               .css-6qob1r.e1fqkh3o3{
                    margin-top: -75px;
               }
               .css-1544g2n.eczjsme4{
                    margin-top: -75px;
               }
        </style>
        """, unsafe_allow_html=True)

    data_list = ['bus1', 'bus2']
    option = 'bus1'
    st.session_state.df0 = st.session_state.df1

    column_list = st.session_state.df0.columns[3:].values
    #column_list_selector = st.sidebar.multiselect("停留所", column_list, default = column_list)
    df_list('始発時分')
    index_selector = st.sidebar.multiselect("出発時間", st.session_state.df_list, default = st.session_state.df_list, key = "time", on_change = change_around_time)

    #サイドバー作成用
    #[6,7,8]時台
    if st.session_state.flag == "A":
        df_list('時台')
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

    if st.session_state.flag == 1:
        st.session_state.select_arr = st.session_state.df0[
                                            (
                                            st.session_state.df0["時台"].isin(around_time_selector)
                                            & st.session_state.df0["終点"].isin(end_point_selector)
                                            & st.session_state.df0["始発時分"].isin(index_selector)
                                            )
                                        ][column_list]
    
        st.session_state.select_arr1 = st.session_state.df0[
                                            (
                                            st.session_state.df0["時台"].isin(around_time_selector)
                                            & st.session_state.df0["終点"].isin(end_point_selector)
                                            & st.session_state.df0["始発時分"].isin(index_selector)
                                            )
                                        ]
    else:
        st.session_state.select_arr = st.session_state.df0[
                                            (
                                            st.session_state.df0["終点"].isin(end_point_selector)
                                            & st.session_state.df0["始発時分"].isin(index_selector)
                                            )
                                        ][column_list]
    
        st.session_state.select_arr1 = st.session_state.df0[
                                            (
                                            st.session_state.df0["終点"].isin(end_point_selector)
                                            & st.session_state.df0["始発時分"].isin(index_selector)
                                            )
                                        ]
        
    
    fig = go.Figure()
    for i in range(len(st.session_state.select_arr.index)):
        fig.add_traces(go.Scatter(x = st.session_state.select_arr.columns.values,
                          y = st.session_state.select_arr.T[st.session_state.select_arr.index[i]],
                          name = index_selector[i])
                )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig)
    # データ表示用
    st.dataframe(st.session_state.select_arr1)

# ページ判定
if st.session_state.page_id == -1:
    main_page()
