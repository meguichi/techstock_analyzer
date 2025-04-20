# gpt_advice.py
from openai import OpenAI
import streamlit as st
import os

# APIクライアントの初期化
# 先に環境変数を確認、次に secrets を試す（順序が重要！）
api_key = os.getenv("OPENAI_API_KEY")

try:
    if not api_key:
        api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass  # secrets.toml が存在しない環境でも落ちないように

if not api_key:
    st.error("❌ OpenAIのAPIキーが見つかりません。環境変数または .streamlit/secrets.toml に設定してください。")
    st.stop()

client = OpenAI(api_key=api_key)
if not api_key:
    st.error("❌ OpenAIのAPIキーが設定されていません。secrets.toml か 環境変数に設定してください。")
    st.stop()

client = OpenAI(api_key=api_key)
def generate_advice(data_dict):
    messages = []
    for ticker, df in data_dict.items():
        latest_rsi = df['RSI'].dropna().iloc[-1]
        latest_close = df['Close'].iloc[-1]
        messages.append(f"{ticker} の直近終値は {latest_close:.2f} 円、RSIは {latest_rsi:.2f} です。")

    prompt = "以下は複数の株式のテクニカル分析の要約です。それを元に今後の投資アドバイスを日本語で簡潔に出してください。\n" + "\n".join(messages)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは株式アナリストです。"},
                {"role": "user", "content": prompt}
            ]
        )
        advice = response.choices[0].message.content
        st.subheader("🤖 ChatGPTからのアドバイス")
        st.write(advice)
    except Exception as e:
        st.error("ChatGPTによるアドバイス生成に失敗しました。")
        st.exception(e)
