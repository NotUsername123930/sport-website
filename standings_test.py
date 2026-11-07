import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPORT_API_KEY")

url = "https://v3.football.api-sports.io/standings"

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "league": 39,
    "season": 2024
}

response = requests.get(url,headers=headers,params=params)

data = response.json()

table = data["response"][0]["league"]["standings"][0]

for team in table[:5]:
    print(team)