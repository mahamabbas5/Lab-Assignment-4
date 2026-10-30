
from flask import Flask, request, jsonify
from scraper import search_article
from summarizer import summarize_text

app = Flask(__name__)

REGISTRATION = "FA23-BDS-019"
NEWS_SOURCE = "MIT Technology Review"


@app.route("/", methods=["GET"])
def home():
    return f"""
    <html>
        <head>
            <title>DevOps News Scraper</title>
        </head>
        <body style="font-family: Arial; text-align: center;
                     margin-top: 100px;">
            <h1>MIT Technology Review News Scraper</h1>
            <h2>Registration Number: {REGISTRATION}</h2>
            <h3>News Source: {NEWS_SOURCE}</h3>
            <p>Use the API endpoint below to search for news.</p>
            <p>/get?keyword=AI</p>
        </body>
    </html>
    """


@app.route("/get", methods=["GET"])
def get_news():
    keyword = request.args.get("keyword", "").strip()

    if not keyword:
        return jsonify({
            "error": "Please provide a keyword."
        }), 400

    try:
        article = search_article(keyword)
        summary = summarize_text(article["content"])

        return jsonify({
            "registration": REGISTRATION,
            "newssource": NEWS_SOURCE,
            "keyword": keyword,
            "url": article["url"],
            "summary": summary
        })

    except Exception as error:
        return jsonify({
            "error": str(error),
            "registration": REGISTRATION,
            "newssource": NEWS_SOURCE,
            "keyword": keyword
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=False
    )

