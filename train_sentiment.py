from get_youtube_api import getYoutubeData
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
class TrainSentiment:
    def __init__(self,model= SentimentIntensityAnalyzer()):
        self.model = model
   
    def analyze_sentiment(self, url):
        self.df = getYoutubeData(youtube_url=url).to_dataframe()
        sentiments = []
        for comment in self.df["text"]:
            result = self.model.polarity_scores(comment)
            if result['compound'] >= 0.05:
                sentiments.append("Positive")
            elif result['compound'] <= -0.05:
                sentiments.append("Negative")
            else:
                sentiments.append("Neutral")

        self.df["sentiment"] = sentiments
        return self.df

    def show_results(self, url):
        df = self.analyze_sentiment(url)

        positive_count = (df["sentiment"].str.lower() == "positive").sum()
        negative_count = (df["sentiment"].str.lower() == "negative").sum()
        neutral_count = (df["sentiment"].str.lower() == "neutral").sum()

        df_positive = df[df["sentiment"].str.lower() == "positive"]
        df_negative = df[df["sentiment"].str.lower() == "negative"]
        df_neutral = df[df["sentiment"].str.lower() == "neutral"]

        return {
            "Positive": positive_count,
            "Negative": negative_count,
            "Neutral": neutral_count,
            "df_positive": df_positive,
            "df_negative": df_negative,
            "df_neutral": df_neutral,
            "df": df
        }
    def bar_chart(self, df):
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
    def pie_chart(self, df):
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
