from flask import Flask, jsonify
import requests
import os
from openai import OpenAI

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "business",
        "language": "en",
        "apiKey": NEWS_API_KEY,
        "pageSize": 5
    }
    return requests.get(url, params=params).json()

def analyze(text):
    prompt = f"""
วิเคราะห์ข่าวนี้สำหรับนักลงทุนและตอบเป็นภาษาไทย:
{text}

ตอบเป็นหัวข้อ:
- สรุปข่าว
- ผลกระทบระยะสั้น
- ผลกระทบระยะยาว
- หุ้นที่ได้ประโยชน์
- หุ้นที่เสียประโยชน์
- Market Sentiment
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    news = get_news()
    results = []
    for article in news["articles"]:
        analysis = analyze(article["title"] + article["description"])
        results.append({
            "title": article["title"],
            "analysis": analysis
        })
    return jsonify(results)