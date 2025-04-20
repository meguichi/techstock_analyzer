# login.py（bcrypt → hashlib に置き換え）
import streamlit as st
import json
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

def load_credentials():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['credentials']

def write_login_log(username):
    with open('login_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.now()} - {username}がログインしました。\n")

def login_page():
    st.title("ログイン画面🌸")
    credentials = load_credentials()

    with st.form("login_form"):
        username = st.text_input("ユーザー名", autocomplete='off')
        password = st.text_input("パスワード", type='password', autocomplete='off')
        submitted = st.form_submit_button("ログイン")

        if submitted:
            if username in credentials:
                stored_hash = credentials[username]["password"]
                if check_password(password, stored_hash):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    write_login_log(username)
                    st.rerun()
                else:
                    st.error("パスワードが間違っています。")
            else:
                st.error("ユーザー名が存在しません。")
