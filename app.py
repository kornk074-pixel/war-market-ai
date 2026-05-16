from flask import Flask, jsonify, render_template
import openai
import requests

app = Flask(__name__)

openai.api_key = "OPENAI_API_KEY"

NEWS_API = "https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey=bcf41776a1fe4fa68397dca719525c45"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news")
def get_news():
    news = requests.get(NEWS_API).json()
    articles = news["articles"][:5]

    text = ""
    for a in articles:
        text += a["title"] + "\n" + a["description"] + "\n\n"

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

app.run(host="0.0.0.0", port=10000)