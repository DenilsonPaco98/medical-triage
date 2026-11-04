"""Dashboard streamlit application."""

import streamlit as st

st.set_page_config(
    page_title="Medical Review Sentiment",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Medical Review Sentiment Analysis")
st.markdown("""
Welcome to the Medical Review Sentiment Analysis Dashboard!

This application analyzes the sentiment of medical reviews using a fine-tuned BERT model.

**Features:**
- 📊 Interactive sentiment analysis
- 📈 Real-time predictions
- 📉 Performance metrics
- 🔍 Data exploration

Select a page from the sidebar to get started.
""")

st.info("""
This is a sample Streamlit dashboard. You can expand it with:
- Sentiment prediction interface
- Historical data visualization
- Model performance metrics
- Batch prediction
""")
