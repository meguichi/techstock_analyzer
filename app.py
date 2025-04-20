# app.py
import streamlit as st
from login import login_page
from dashboard import main_dashboard

# セッション初期化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 表示切り替え
if st.session_state.logged_in:
    main_dashboard()
else:
    login_page()
