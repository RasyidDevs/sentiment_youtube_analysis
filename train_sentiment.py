from get_youtube_api import getYoutubeData
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
class TrainSentiment:
    def __init__(self,model= SentimentIntensityAnalyzer() , API_KEY=None, url=None):
        self.model = model
        self.df = getYoutubeData(youtube_url=url, API_KEY=API_KEY).to_dataframe()

    def analyze_sentiment(self):
        df = self.df
        sentiments = []
        for comment in df["text"]:
            result = self.model.polarity_scores(comment)
            if result['compound'] >= 0.05:
                sentiments.append("Positive")
            elif result['compound'] <= -0.05:
                sentiments.append("Negative")
            else:
                sentiments.append("Neutral")

        df["sentiment"] = sentiments
        return df

    def show_results(self):
        df = self.analyze_sentiment()

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
