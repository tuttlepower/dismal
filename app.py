from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import random
import Paper
from articleDAO import getArticles, getNasa
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/econ")
def econ():
    url = "https://back.nber.org/rss/new.xml"
    nber = getArticles(url)

    url = 'https://apps.bea.gov/rss/rss.xml'
    bea = getArticles(url)

    articles = bea + nber

    return render_template("topic.html", topic='Economics', articles = articles)


@app.route("/ml")
def machineLearning():
    url = "https://jmlr.org/jmlr.xml"
    articles = getArticles(url)
    return render_template("topic.html", topic='ML/AI', articles = articles)


@app.route("/cs")
def computerScience():
    return render_template("topic.html", topic='Computer Science')


@app.route("/space")
def space():
    images = getNasa()
    return render_template("space.html", topic='Space' , images = images)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # returns a 200 (not a 404) with the following contents:
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
