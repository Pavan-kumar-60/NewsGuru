from Search_agent.search_agent import Latest_news
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    matter = request.form["matter"]
    news = Latest_news(matter)

    # Return the news as JSON for the frontend to render
    return jsonify(news)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
