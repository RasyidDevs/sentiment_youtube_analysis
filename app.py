import streamlit as st
from get_youtube_api import getYoutubeData 
from train_sentiment import TrainSentiment
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
load_dotenv()  # Load .env file
API_KEY = os.getenv("API_KEY")


def bar_chart(df):
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']

    color_map = {
        'Positive': 'green',
        'Negative': 'red',
        'Neutral': 'gray'
    }

    colors = sentiment_counts['sentiment'].map(color_map).to_list()
    print(colors)
    fig, ax = plt.subplots()

    sentiment_counts.plot(
        x='sentiment',
        y='count',
        kind='bar',
        legend=False,
        color=colors,
        ax=ax
    )

    return fig
def pie_chart(df):
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']

    sentiment_counts['sentiment'] = sentiment_counts['sentiment'].str.capitalize()

    color_map = {
        'Positive': 'green',
        'Negative': 'red',
        'Neutral': 'gray'
    }

    colors = sentiment_counts['sentiment'].map(color_map).tolist()

    fig, ax = plt.subplots()

    sentiment_counts.set_index('sentiment')['count'].plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        ax=ax,
        legend=False
    )

    ax.set_ylabel('')  # hilangkan label default
    ax.set_title("Sentiment Distribution")

    return fig



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
    with st.spinner("Loading.. this may take a while"):
        tr = TrainSentiment(API_KEY=API_KEY, url=url)
        get_youtube = getYoutubeData(youtube_url = url, API_KEY=API_KEY)
        video_id = get_youtube.get_video_id()
        if video_id:
            get_data = tr.show_results()
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
    dropdown = st.selectbox("Select chart type:", options=["pie_chart", "bar_chart"], key="dropdown")

    if dropdown == "pie_chart":
        st.subheader("Pie Chart of Sentiment")
        st.pyplot(pie_chart(df)) 
    else:
        st.subheader("Bar Chart of Sentiment")
        st.pyplot(bar_chart(df))

else:
    st.info("Please enter a YouTube channel URL and click Submit to see sentiment analysis.")
