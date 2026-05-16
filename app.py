from flask import Flask, jsonify, render_template
import openai
import requests
import os

app = Flask(__name__)

# ดึง API KEY จาก Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news")
def get_news():
    news = requests.get(NEWS_API).json()
    articles = news["articles"][:5]

    text = ""
    for a in articles:
        text += a["title"] + "\n" + str(a["description"]) + "\n\n"

    prompt = f"""
แปลข่าวและวิเคราะห์:
- สรุปข่าวเป็นภาษาไทย
- ใครได้ประโยชน์ (หุ้น/ประเทศ)
- ใครเสียประโยชน์ (หุ้น/ประเทศ)

ข่าว:
{text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({"result": response.choices[0].message.content})

# สำคัญมากสำหรับ Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)