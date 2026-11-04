import os
import requests
from dotenv import load_dotenv

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "football_hub.settings"
)

import django
django.setup()

from core.models import News

load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")

URL = "https://gnews.io/api/v4/search"

params = {
    "q": "football",
    "lang": "en",
    "max": 10,
    "apikey": API_KEY
}

response = requests.get(URL, params=params)

data = response.json()

articles = data.get("articles", [])

saved_news = 0

for article in articles:

    News.objects.update_or_create(
        news_id=article["id"],
        defaults={
            "title": article["title"],
            "description": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
            "article_url": article.get("url", ""),
            "image_url": article.get("image", ""),
            "sport": "Football",
            "published_at": article.get("publishedAt"),
        }
    )

    saved_news += 1

print(f"Збережено новин: {saved_news}")