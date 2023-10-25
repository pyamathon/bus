import streamlit as st
import numpy as np
import pandas as pd
import sentencepiece
from transformers import BertJapaneseTokenizer, BertModel
# from sentence_transformers import SentenceTransformer
# from sentence_transformers import models
import torch

# 日本語対応パッケージのインストール
st.title("質問箱")

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
st.session_state.df = pd.read_csv('dict.csv')

def sentence_to_vector(model, tokenizer, sentence):
    # 文を単語に区切って数字にラベル化
    tokens = tokenizer(sentence)["input_ids"]
    # BERTモデルの処理のためtensor型に変換
    input = torch.tensor(tokens).reshape(1,-1)
    # BERTモデルに入力し文のベクトルを取得
    with torch.no_grad():
        outputs = model(input, output_hidden_states=True)
        last_hidden_state = outputs.last_hidden_state[0]
        st.session_state.averaged_hidden_state = last_hidden_state.sum(dim=0) / len(last_hidden_state)
    return st.session_state.averaged_hidden_state

def cosine_similarity(x1, x2, eps): # dimは単純化のため省略
    w12 = torch.sum(x1 * x2)
    w1 = torch.sum(x1 * x1)
    w2 = torch.sum(x2 * x2)
    n12 = (w1 * w2).clamp_min_(eps * eps).sqrt_()
    score = w12 / n12
    st.session_state.score = score.item()

def calc_similarity(sentence1, sentence2):
    sentence_vector1 = sentence_to_vector(model, tokenizer, sentence1)
    sentence_vector2 = sentence_to_vector(model, tokenizer, sentence2)
    cosine_similarity(sentence_vector1, sentence_vector2, 1e-8)
    return st.session_state.score

user_msg = st.chat_input("質問、要望等あれば入力してください")
if user_msg:
    st.session_state.sentence1 = user_msg
    st.session_state.similar_value = 0
    st.session_state.similar_word = ""
    
    for i in range(60):
        st.session_state.sentence2 = ""
        st.session_state.value = 0
        st.session_state.sentence2 = st.session_state.df["question"][i]
        st.session_state.value = calc_similarity(st.session_state.sentence1, st.session_state.sentence2)
        if st.session_state.value > st.session_state.similar_value:
            st.session_state.similar_value = st.session_state.value
            st.session_state.similar_word = st.session_state.df["answer"][i]

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
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": st.session_state.similar_word})
