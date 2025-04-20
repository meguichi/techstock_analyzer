# gpt_advice.py
from openai import OpenAI
import streamlit as st
import os

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
        
def generate_advice(data_dict):
    messages = []
    for ticker, df in data_dict.items():
        try:
            latest_rsi = df['RSI'].dropna().iloc[-1]
            latest_close = df['Close'].iloc[-1]
            messages.append(f"{ticker} の直近終値は {latest_close:.2f} 円、RSIは {latest_rsi:.2f} です。")
        except Exception as e:
            st.warning(f"{ticker} のデータ整形に失敗しました: {e}")

    if not messages:
        st.warning("有効なデータが見つかりませんでした。")
        return

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



