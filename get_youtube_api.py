import re
import requests
import pandas as pd
import html
from bs4 import BeautifulSoup

class getYoutubeData:
    def __init__(self, youtube_url=None):
        self.youtube_url = youtube_url

    def get_video_id(self):
        patterns = [
            r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)",
            r"(?:https?://)?youtu\.be/([^?&]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/embed/([^?&]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/v/([^?&]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([^?&]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/live/([^?&]+)",
            r"(?:https?://)?(?:www\.)?youtube\.com/attribution_link\?.*v%3D([^%&]+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None

    def clean_html(self, raw_html):
        return BeautifulSoup(raw_html, "html.parser").get_text()

    def get_comments(self):
        base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": self.get_video_id(),
            "key": "AIzaSyC6cHq4XRZzF-4sJTlO7Ndh3R1s1pJOEJ0",
            "maxResults": 100
        }

        all_comments = {"comment": []}
        while True:
            response = requests.get(base_url, params=params)
            data = response.json()

            if "items" not in data:
                break
            for item in data["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comment_data = {
                    "text": self.clean_html(html.unescape(snippet["textDisplay"])),
                    "author": snippet["authorDisplayName"],
                    "publishedAt": snippet["publishedAt"],
                    "likeCount": snippet["likeCount"],
                }
                all_comments["comment"].append(comment_data)

            if "nextPageToken" in data:
                params["pageToken"] = data["nextPageToken"]
            else:
                break

        return all_comments

    def to_dataframe(self):
        comments = self.get_comments()
        if comments and "comment" in comments:
            df = pd.DataFrame(comments["comment"])
            return df
        else:
            return pd.DataFrame(columns=["text", "author", "publishedAt", "likeCount"])
    def get_video_stats(self):
        video_id = self.get_video_id()
        base_url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet",
            "id": video_id,
            "key": "AIzaSyC6cHq4XRZzF-4sJTlO7Ndh3R1s1pJOEJ0"
        }

        response = requests.get(base_url, params=params)
        data = response.json()


        snippet = data["items"][0]["snippet"]

        video_info = {
            "title": snippet.get("title", ""),
            "channelTitle": snippet.get("channelTitle", ""),
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", "")
        }

        return video_info

        
