import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


def get_youtube_channel_data(channel_id: str):
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        return {
            "platform": "YouTube",
            "status": "error",
            "message": "YOUTUBE_API_KEY is not configured",
        }

    if not channel_id:
        return {
            "platform": "YouTube",
            "status": "error",
            "message": "YouTube channel ID is required",
        }

    try:
        youtube = build(
            "youtube",
            "v3",
            developerKey=api_key,
        )

        response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id,
        ).execute()

        if not response.get("items"):
            return {
                "platform": "YouTube",
                "status": "error",
                "message": "YouTube channel not found",
            }

        channel = response["items"][0]
        statistics = channel.get("statistics", {})
        snippet = channel.get("snippet", {})

        return {
            "platform": "YouTube",
            "status": "connected",
            "channel_id": channel.get("id"),
            "channel_name": snippet.get("title"),
            "followers": int(statistics.get("subscriberCount", 0)),
            "views": int(statistics.get("viewCount", 0)),
            "videos": int(statistics.get("videoCount", 0)),
        }

    except HttpError as error:
        return {
            "platform": "YouTube",
            "status": "error",
            "message": f"YouTube API error: {error}",
        }

    except Exception as error:
        return {
            "platform": "YouTube",
            "status": "error",
            "message": str(error),
        }


def get_social_media_data(platform: str = None):
    youtube_data = get_youtube_channel_data(
        os.getenv("YOUTUBE_CHANNEL_ID")
    )

    return {
        "platforms": [
            {
                "platform": "Instagram",
                "followers": 1000,
                "likes": 250,
                "comments": 50,
                "shares": 25,
                "views": 5000,
            },
            youtube_data,
            {
                "platform": "TikTok",
                "followers": 1500,
                "likes": 400,
                "comments": 80,
                "shares": 60,
                "views": 8000,
            },
        ]
    }
