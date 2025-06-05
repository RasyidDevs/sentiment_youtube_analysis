import streamlit as st
from get_youtube_api import getYoutubeData 
from train_sentiment import TrainSentiment

API_KEY = "AIzaSyC6cHq4XRZzF-4sJTlO7Ndh3R1s1pJOEJ0"

tr = TrainSentiment()
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: rgba(255, 255, 255, 0.3);
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    z-index: 9999;
}
</style>

<div class="footer">
    © Made by rasyid bomantoro. all rights reserved.
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
# Sidebar input
with st.sidebar:
    st.markdown(
        '<h1><span style="color:#1f77b4;">RASYT</span> AI🤖</h1>',
        unsafe_allow_html=True
    )
    url = st.text_input("Enter link youtube video", key="username")
    submit = st.button("Submit", key="submit")
st.markdown(
    '<h1><span style="color:#1f77b4;">RASYT</span> AI🤖</h1>',
    unsafe_allow_html=True
)
if submit and url:
    get_youtube = getYoutubeData(url)
    video_id = get_youtube.get_video_id()
    if video_id:
        with st.spinner("Loading.. this may take a while"):
            get_data = tr.show_results(url)
            # Simpan di session_state
            st.session_state["df"] = get_data["df"]
            st.session_state["stat"] = get_youtube.get_video_stats()
            st.session_state["summary"] = {
                "Positive": get_data["Positive"],
                "Negative": get_data["Negative"],
                "Neutral": get_data["Neutral"],
                "Total": len(get_data["df"])
            }
        st.success("Data loaded successfully!")
    else:
        st.error("Invalid YouTube channel URL or no videos found.")

# Tampilkan data dan grafik hanya jika data sudah ada di session_state
if "df" in st.session_state and "summary" in st.session_state and "stat" in st.session_state:
    summary = st.session_state["summary"]
    df = st.session_state["df"]
    stat = st.session_state["stat"]
    st.title("Sentiment Analysis of YouTube Comments")
    st.subheader("Video Information")
    st.image(stat["thumbnail"], use_container_width=True)
    st.write("Video Title:", stat["title"])
    st.write("Channel Title:", stat["channelTitle"])
    st.write("Total Comments:", summary["Total"])
    st.write("Positive Comments:", summary["Positive"])
    st.write("Negative Comments:", summary["Negative"])
    st.write("Neutral Comments:", summary["Neutral"])
    st.dataframe(df)
    # Dropdown untuk memilih jenis chart
    dropdown = st.selectbox("Select chart type:", options=["pie_chart", "bar_chart"], key="dropdown")

    if dropdown == "pie_chart":
        st.subheader("Pie Chart of Sentiment")
        st.pyplot(tr.pie_chart(df)) 
    else:
        st.subheader("Bar Chart of Sentiment")
        st.pyplot(tr.bar_chart(df))

else:
    st.info("Please enter a YouTube channel URL and click Submit to see sentiment analysis.")
