import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from predict import predict_news
from credibility import source_score
from scraper import extract_article
from explain import explain_prediction
from style_detector import detect_clickbait
from trend_analysis import top_words
from news_fetcher import get_trending_news

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="CREDIFY",
    layout="wide",
    page_icon="📰"
)

# =============================
# PROFESSIONAL UI STYLE
# =============================
st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#eef2f3,#dfe9f3);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* MAIN TITLE */
.main-title{
    text-align:center;
    font-size:64px;
    font-weight:900;
    color:#1f2937;
    margin-bottom:5px;
}

/* SUBTITLE */
.subtitle{
    text-align:center;
    font-size:24px;
    color:#555;
    margin-bottom:50px;
}


.feature-card:hover{
    transform: translateY(-5px);
}

/* CARD TITLE */
.feature-card h3{
    font-size:28px;
    margin-bottom:12px;
    font-weight:700;
}

/* CARD TEXT */
.feature-card p{
    font-size:18px;
    color:#555;
}

/* PAGE HEADERS */
h1{
    font-size:40px !important;
}
h2{
    font-size:32px !important;
}
h3{
    font-size:28px !important;
}

/* BIG BUTTON */
.stButton>button{
    padding: 12px 20px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 12px;
    background-color: #1f2937;
    color: white;
}
.stButton>button:hover{
    background-color:#374151;
}
</style>
""", unsafe_allow_html=True)

# =============================
# SESSION NAVIGATION
# =============================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =============================
# HOME PAGE
# =============================
if st.session_state.page == "home":

    # Gamified CREDIFY title
    st.markdown("""
    <h1 style="
        text-align:center; 
        font-size:72px; 
        font-weight:900; 
        background: linear-gradient(90deg, #ff6ec4, #7873f5, #42e695);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 2s linear infinite;
        margin-bottom:5px;
        ">
           CREDIFY
    </h1>

    <style>
    @keyframes shine {
        0% { background-position: -500% 0; }
        100% { background-position: 500% 0; }
    }
    </style>

    <p class="subtitle">Where Facts Matter</p>
    """, unsafe_allow_html=True)

    # =============================
    # FEATURE CARDS
    # =============================
    col1, col2, col3 = st.columns(3, gap="large")

    # Dataset Insights
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Dataset Insights")
        st.write("Explore training dataset statistics and distribution.")
        if st.button("Open Dataset Dashboard", use_container_width=True, key="dataset"):
            st.session_state.page = "dataset"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Live Trending News
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌍 Live Trending News")
        st.write("Scan trending headlines and detect misinformation.")
        if st.button("Open Trending Scanner", use_container_width=True, key="trending"):
            st.session_state.page = "trending"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Analyze News Article
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 Analyze News Article")
        st.write("Check whether an article is real or fake.")
        if st.button("Open News Analyzer", use_container_width=True, key="analyze"):
            st.session_state.page = "analyze"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# =============================
# DATASET PAGE
# =============================
elif st.session_state.page == "dataset":

    st.title("📊 Dataset Overview")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

    data = {"Type": ["Fake News", "Real News"], "Count": [23481, 21417]}
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Type",
        y="Count",
        color="Type",
        text="Count",
        title="Training Dataset Distribution"
    )
    fig.update_layout(title_font_size=26)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Dataset Size: **44,898 labeled news articles used for model training**")

# =============================
# TRENDING NEWS PAGE
# =============================
elif st.session_state.page == "trending":

    st.title("🌍 Live Trending News Scanner")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

    if "trending_news" not in st.session_state:
        st.session_state.trending_news = []

    # Big, centered Fetch button
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("Fetch Trending News", key="fetch_trending"):
        st.session_state.trending_news = get_trending_news()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.trending_news:

        for i, news in enumerate(st.session_state.trending_news):
            st.subheader(news["title"])

            if st.button("Analyze", key=f"analyze_{i}"):

                article_text = extract_article(news["link"])
                if article_text is None or len(article_text) < 200:
                    article_text = news["title"]

                label, prob = predict_news(article_text)
                fake_prob = prob[0]
                real_prob = prob[1]

                if label == "Fake News":
                    st.error(f"⚠️ Fake News ({round(fake_prob*100,2)}%)")
                else:
                    st.success(f"✅ Real News ({round(real_prob*100,2)}%)")

                st.progress(int(fake_prob*100))

# =============================
# ANALYZE ARTICLE PAGE
# =============================
elif st.session_state.page == "analyze":

    st.title("🧠 News Analysis")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

    text = st.text_area("Paste News Article", height=200)
    url = st.text_input("Or Enter News URL")

    if st.button("Analyze News"):

        if url != "":
            text = extract_article(url)

        if text == "":
            st.warning("Enter article text or URL")

        else:
            label, prob = predict_news(text)
            fake_prob = prob[0]
            real_prob = prob[1]

            if label == "Fake News":
                st.error("⚠️ Fake News Detected")
            else:
                st.success("✅ Real News Detected")

            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Fake Probability",
                "Source Credibility",
                "Writing Style",
                "Risk Score",
                "Key Terms",
                "AI Explanation"
            ])

            with tab1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=fake_prob * 100,
                    title={'text': "Fake Probability"},
                    gauge={'axis': {'range': [0, 100]}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                score = source_score(url) if url != "" else 50
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={'text': "Source Credibility"},
                    gauge={'axis': {'range': [0, 100]}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            with tab3:
                clickbait = detect_clickbait(text)
                st.write("Clickbait Score:", clickbait)
                if clickbait >= 4:
                    st.error("Highly sensational writing detected")
                elif clickbait >= 2:
                    st.warning("Moderate clickbait writing detected")
                else:
                    st.success("Neutral journalistic writing style")

            with tab4:
                risk = (fake_prob * 100) * 0.7 + (100 - score) * 0.3
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk,
                    title={'text': "Fake News Risk"},
                    gauge={'axis': {'range': [0, 100]}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            with tab5:
                words = top_words(text)
                for w, c in words[:10]:
                    st.write(f"{w} : {c}")

            with tab6:
                explanation = explain_prediction(text)
                for word, weight in explanation[:10]:
                    st.write(f"{word} → influence score {round(weight,3)}")