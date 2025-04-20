import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

def plot_stock_charts(data_dict):
    for ticker, df in data_dict.items():
        st.subheader(f"📈 {ticker} のチャート")
        fig, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(df.index, df['Close'], label='終値', linewidth=1.5)
        ax1.plot(df.index, df['MA25'], label='MA25', linestyle='--')
        ax1.plot(df.index, df['MA75'], label='MA75', linestyle=':')
        ax1.set_title(f"{ticker} - 終値と移動平均")
        ax1.legend()
        st.pyplot(fig)

        st.markdown("**RSI**")
        fig, ax2 = plt.subplots(figsize=(10, 2))
        ax2.plot(df.index, df['RSI'], label='RSI', color='purple')
        ax2.axhline(70, color='red', linestyle='--')
        ax2.axhline(30, color='blue', linestyle='--')
        ax2.set_ylim(0, 100)
        st.pyplot(fig)

def show_correlation_heatmap(data_dict):
    st.subheader("📊 銘柄間の相関ヒートマップ")
    price_df = pd.DataFrame({ticker: df['Close'] for ticker, df in data_dict.items()})
    corr = price_df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)