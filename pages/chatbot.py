import streamlit as st
import numpy as np
import pandas as pd
from gradio_client import Client

# 日本語対応パッケージのインストール
st.title("質問箱")

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
st.session_state.df = pd.read_csv('dict.csv')

user_msg = st.chat_input("質問、要望等あれば入力してください")
if user_msg:
    client = Client("https://huggingface.co/spaces/pyamath/chatbot2")
    result = client.predict(
        user_msg,	# str  in 'user_msg' Textbox component
        api_name="/predict"
    )
    
    st.session_state.similar_word = result[0]
    st.session_state.value = result[1]

    st.write(st.session_state.value)
        
    # for i in range(60):
    #     st.session_state.sentence2 = ""
    #     st.session_state.value = 0
    #     st.session_state.sentence2 = st.session_state.df["question"][i]
    #     client = Client("https://pyamath-chatbot.hf.space")
    #     result = client.predict(
    #         user_msg,	# str  in 'user_msg' Textbox component
    #         api_name="/predict"
    #     )
    #     st.session_state.value = result[1]
    #     if st.session_state.value > st.session_state.similar_value:
    #         st.session_state.similar_value = st.session_state.value
    #         st.session_state.similar_word = st.session_state.df["answer"][i]

    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のメッセージを表示
    assistant_msg = "もう一度入力してください"
    with st.chat_message(USER_NAME):
        st.write(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        st.write(st.session_state.similar_word)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": user_msg})
