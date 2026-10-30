import os
import requests
from dotenv import load_dotenv
from datetime import date

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "football_hub.settings")

import django
django.setup()

from core.models import Fixture

# Завантажуємо ключ з .env
load_dotenv()

API_KEY = os.getenv("SPORT_API_KEY")

if not API_KEY:
    raise ValueError("Помилка: SPORT_API_KEY не знайдено у файлі .env!")

URL = "https://v3.football.api-sports.io/fixtures"

TARGET_LEAGUES = {
    39: "Англійська Прем'єр-ліга",
    140: "Іспанська Ла Ліга",
    135: "Італійська Серія А",
    78: "Німецька Бундесліга",
    61: "Французька Ліга 1",
    2: "Ліга чемпіонів УЄФА",
    3: "Ліга Європи УЄФА",
    847: "Ліга конференцій УЄФА",
}

querystring = {
    "date": date.today().strftime("%Y-%m-%d")
}

headers = {
    "x-apisports-key": API_KEY
}

try:
    print("Отримання матчів...")

    response = requests.get(
        URL,
        headers=headers,
        params=querystring
    )

    response.raise_for_status()

    data = response.json()

    fixtures = data.get("response", [])

    saved_matches = 0

    for item in fixtures:

        league_id = item.get("league", {}).get("id")

        if league_id not in TARGET_LEAGUES:
            continue

        fixture_id = item.get("fixture", {}).get("id")

        league_name = TARGET_LEAGUES[league_id]

        home_team = item.get("teams", {}).get("home", {}).get("name")
        away_team = item.get("teams", {}).get("away", {}).get("name")

        status = item.get("fixture", {}).get("status", {}).get("short")

        home_goals = item.get("goals", {}).get("home")
        away_goals = item.get("goals", {}).get("away")

        Fixture.objects.update_or_create(
            api_id=fixture_id,
            defaults={
                "league_name": league_name,
                "home_team": home_team,
                "away_team": away_team,
                "status": status,
                "home_score": home_goals,
                "away_score": away_goals,
            }
        )

        saved_matches += 1

        print(
            f"Збережено: "
            f"{home_team} - {away_team}"
        )

    print(f"\nУспішно оброблено {saved_matches} матчів.")

except requests.exceptions.RequestException as e:
    print(f"Помилка API: {e}")