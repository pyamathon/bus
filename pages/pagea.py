import streamlit as st

st.write("Page A")
st.session_state.a = 1
st.write(st.session_state.a)
