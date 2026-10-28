import os
import requests
from dotenv import load_dotenv

# Завантажуємо ключ з твого безпечного файлу .env
load_dotenv()
API_KEY = os.getenv("SPORT_API_KEY")
URL = "https://v3.football.api-sports.io/fixtures"

if not API_KEY:
    raise ValueError("Помилка: SPORT_API_KEY не знайдено у файлі .env!")

# Словник елітних турнірів FOOTY та їхні залізні ID з бази даних API-Football
TARGET_LEAGUES = {
    39: "Англійська Прем'єр-ліга",
    140: "Іспанська Ла Ліга",
    135: "Італійська Серія А",
    78: "Німецька Бундесліга",
    61: "Французька Ліга 1",
    2: "Ліга чемпіонів УЄФА",
    3: "Ліга Європи УЄФА",
    847: "Ліга конференцій УЄФА"
}

# Параметри запиту на сьогоднішню дату
querystring = {"date": "2026-10-28"}
headers = {"x-apisports-key": API_KEY}

try:
    print("З'єднуємось із сервером та фільтруємо 484 матчі...")
    response = requests.get(URL, headers=headers, params=querystring)
    response.raise_for_status()

    data = response.json()
    all_fixtures = data.get("response", [])

    print("\n=== АКТУАЛЬНІ МАТЧІ ТОП-ЛІГ ТА ЄВРОКУБКІВ ДЛЯ FOOTY ===")

    found_target_matches = 0

    for item in all_fixtures:
        league_id = item.get("league", {}).get("id")

        # Перевіряємо, чи входить ID турніру в наш список обраних
        if league_id in TARGET_LEAGUES:
            found_target_matches += 1

            league_name = TARGET_LEAGUES[league_id]
            home_team = item.get("teams", {}).get("home", {}).get("name")
            away_team = item.get("teams", {}).get("away", {}).get("name")

            # Статус матчу (NS - не розпочався, FT - завершено, 1H/2H - йде прямо зараз)
            status = item.get("fixture", {}).get("status", {}).get("short")

            # Рахунок
            home_goals = item.get("goals", {}).get("home")
            away_goals = item.get("goals", {}).get("away")

            # Якщо матч ще не розпочався, красиво пишемо "vs" замість порожнього рахунку
            if status == "NS":
                score = "vs"
            else:
                score = f"{home_goals}:{away_goals}"

            print(f"[{league_name}] {home_team} {score} {away_team} (Статус: {status})")

    if found_target_matches == 0:
        print("\nСьогодні матчів у наших 5 топ-лігах та єврокубках немає.")
        print("Це нормальна ситуація для середини тижня, якщо немає туру Ліги Чемпіонів. Чекаємо вихідних!")
    else:
        print(f"\nФільтрація завершена! Знайдено {found_target_matches} важливих поєдинків для головної сторінки.")

except requests.exceptions.RequestException as e:
    print(f"Помилка підключення до API: {e}")
