import os
import requests
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "football_hub.settings")

import django
django.setup()

from core.models import News

load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")
URL = "https://gnews.io/api/v4/search"

TOPICS = [
    "UEFA Champions League",
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "soccer transfer"
]

KEYWORDS = [
    "uefa",
    "fifa",
    "champions league",
    "premier league",
    "la liga",
    "serie a",
    "bundesliga",
    "transfer",
    "world cup"
]

saved_news = 0

for topic in TOPICS:
    params = {
        "q": topic,
        "lang": "en",
        "max": 10,
        "apikey": API_KEY
    }

    response = requests.get(URL, params=params)
    data = response.json()
    articles = data.get("articles", [])

    for article in articles:
        text = (
            article.get("title", "") + " " +
            article.get("description", "")
        ).lower()

        if not any(keyword in text for keyword in KEYWORDS):
            continue

        News.objects.update_or_create(
            news_id=article["id"],
            defaults={
                "title": article["title"],
                "description": article.get("description", ""),
                "source": article.get("source", {}).get("name", ""),
                "article_url": article.get("url", ""),
                "image_url": article.get("image", ""),
                "sport": "soccer",
                "published_at": article.get("publishedAt"),
            }
        )

        saved_news += 1

print(f"Збережено новин: {saved_news}")