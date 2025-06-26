from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

# Координаты городов
PREDEFINED_CITIES = {
    "Tashkent": {"lat": 41.3111, "lon": 69.2797},
    "Samarkand": {"lat": 39.6542, "lon": 66.9597}
}

def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true&hourly=relative_humidity_2m"
    )
    response = requests.get(url).json()
    weather = response.get("current_weather", {})
    if "hourly" in response and "time" in response["hourly"]:
        try:
            index = response["hourly"]["time"].index(weather["time"])
            weather["humidity"] = response["hourly"]["relative_humidity_2m"][index]
        except:
            weather["humidity"] = "—"
    return weather

@app.route("/", methods=["GET", "POST"])
def index():
    city = ""
    weather = {}
    if request.method == "POST":
        city = request.form["city"].title()
    elif request.args.get("city"):
        city = request.args.get("city").title()

    if city in PREDEFINED_CITIES:
        coords = PREDEFINED_CITIES[city]
        weather = get_weather(coords["lat"], coords["lon"])

    return render_template("index.html", weather=weather, city=city, datetime=datetime)

if __name__ == "__main__":
    app.run(debug=True)
