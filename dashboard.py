# dashboard.py
import streamlit as st
from datetime import datetime
from analysis import fetch_stock_data
from visualize import plot_stock_charts, show_correlation_heatmap
from gpt_advice import generate_advice
from openai import OpenAI
import os
import re

# 🔐 OpenAI APIキーの取得（安全対応）
api_key = os.getenv("OPENAI_API_KEY")
try:
    if not api_key:
        api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = None

client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.warning(f"OpenAIクライアントの初期化に失敗しました: {e}")

# fallback辞書（必要に応じて拡張可能）
manual_ticker_map = {
    "トヨタ": "7203.T",
    "任天堂": "7974.T",
    "ソニー": "6758.T",
    "キーエンス": "6861.T"
}

# ChatGPTで会社名から証券コードを取得（またはfallback）
def get_ticker_from_company_name(name):
    # fallback辞書優先
    if name in manual_ticker_map:
        return manual_ticker_map[name]

    if client is None:
        st.warning("OpenAI APIが使えないため、証券コードの取得をスキップします。")
        return None

    prompt = f"{name} の日本株式の証券コード（形式: 7203.Tなど）を教えてください。証券コードのみを回答してください。"
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは日本の株式市場に詳しい金融アナリストです。出力は証券コードのみ（例: 7203.T）でお願いします。"},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        match = re.search(r'\b\d{4}\.T\b|\^?[A-Z0-9]+\.T\b', content)
        if match:
            return match.group(0)
    except Exception as e:
        st.warning(f"{name} の証券コード取得に失敗しました: {e}")
    return None

# メインダッシュボード
def main_dashboard():
    st.title("📊 テクニカル分析ダッシュボード")

    company_input = st.text_input(
        "会社名（カンマ区切りで複数指定可）",
        value=st.session_state.get("company_input", "")
    )
    st.session_state.company_input = company_input

    selected_tickers = []
    ticker_map = {}

    if st.button("銘柄コードを取得"):
        with st.spinner("銘柄コードを取得中..."):
            for name in st.session_state.company_input.split(","):
                name = name.strip()
                if not name:
                    continue
                code = get_ticker_from_company_name(name)
                if code:
                    ticker_map[code] = name
                else:
                    st.warning(f"❌ {name} のコード取得に失敗しました。")
        st.session_state.ticker_map = ticker_map

    if st.session_state.get("ticker_map"):
        st.markdown("### ✅ 取得された銘柄コード")
        for code, name in st.session_state.ticker_map.items():
            if st.checkbox(f"{code}（{name}）", key=code):
                selected_tickers.append(code)
        st.session_state.selected_tickers = selected_tickers

    if st.session_state.get("selected_tickers"):
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("開始日", datetime(2023, 1, 1))
        with col2:
            end_date = st.date_input("終了日", datetime(2024, 12, 31))

        if st.button("実行"):
            with st.spinner("データ取得と分析中..."):
                try:
                    data_dict = fetch_stock_data(st.session_state.selected_tickers, start_date, end_date)
                    plot_stock_charts(data_dict)
                    show_correlation_heatmap(data_dict)
                    generate_advice(data_dict)
                except Exception as e:
                    st.error("データの取得または処理中にエラーが発生しました。")
                    st.exception(e)
    else:
        st.info("会社名を入力し、銘柄コードを取得してチェックを付けてください。")
