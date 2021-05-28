from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import random
import Paper
from articleDAO import getArticles, getNasa, getArxivFeed

#
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import func


app = Flask(__name__)

#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articlesDB.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#
class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    article = db.Column(db.String(1000))

    def __repr__(self):
        return self.id + "-" + self.article

    def to_string(self):
        return str(self.article)


@app.route("/article", methods = ['GET'])
def get_rand_article():
    #get # of articles as int
    max_number = db.session.query(func.max(Article.id)).scalar()
    
    #grab random ID in range
    article_id = random.randint(0,max_number)

    # get article list
    random_article_query_object = Article.query.filter_by(id=article_id)

    # get list from object
    random_article_list = random_article_query_object.all()

    # filter this list to the 0th
    random_article_object = random_article_list[0]

    # bunch of stuff
    random_article = random_article_object.article

    # or do all this bullshit in one line
    #random_article = Article.query.all()[article_id].article

    return random_article

@app.route("/initialize", methods=['GET'])
def initialize():
    #instance db instance
    db.create_all()
    #iterate through articles file and add them to db
    counter = 0 
    with open('articles.txt')as input_file:
        for line in input_file:
            # create new instance of an article and pefine the values
            article = Article()
            article.id = counter
            article.article = line

            #add to db and commit
            db.session.add(article)
            db.session.commit()

            counter = counter + 1
        # flush connection
        db.session.flush()

    return "db created"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/economics")
def econ():
    articles = []

    url = "https://back.nber.org/rss/new.xml"
    articles = articles + getArticles(url)

    url = 'https://apps.bea.gov/rss/rss.xml'
    articles = articles + getArticles(url)

    url = 'http://export.arxiv.org/rss/econ'
    articles = articles + getArxivFeed(url)

    return render_template("topic.html", topic='Economics', articles=articles)


@app.route("/machinelearning")
def machineLearning():
    url = "https://jmlr.org/jmlr.xml"
    articles = getArticles(url)
    return render_template("topic.html", topic='ML/AI', articles=articles)


@app.route("/computerscience")
def computerScience():
    url = 'http://export.arxiv.org/rss/cs'
    articles = getArxivFeed(url)
    return render_template("topic.html", topic='Computer Science', articles=articles)


@app.route("/space")
def space():
    images = getNasa()
    return render_template("space.html", topic='Space', images=images)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # returns a 200 (not a 404) with the following contents:
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
