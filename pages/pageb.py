import streamlit as st

if "a" not in st.session_state:
    st.session_state.a = 0
st.write(st.session_state.a)
