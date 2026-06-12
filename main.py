import os
import requests
import smtplib

CITY = "Kochi"

API_KEY = os.getenv("WEATHER_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print("API Error:", data)
    exit()

temperature = data["main"]["temp"]
weather = data["weather"][0]["main"]

print(f"Temperature: {temperature}°C")
print(f"Weather: {weather}")

if temperature > 35 or weather.lower() in ["rain", "drizzle", "thunderstorm"]:
    subject = "Weather Alert"
    body = f"""
Weather Alert for {CITY}

Temperature: {temperature} C
Condition: {weather}

Take necessary precautions.
"""

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(
            EMAIL_USER,
            EMAIL_TO,
            message
        )

    print("Alert email sent!")

else:
    print("No alert required.")