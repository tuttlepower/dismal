# Imports
import csv
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

# Paper Object
class Paper:
    def __init__(self, title, description, link, date):
        self.title = title
        self.description = description
        self.link = link
        self.date = date

    def __dict__(self):
        return {
            'Title': self.title,
            'Description': self.description,
            'Link': self.link,
            'Date': self.date
        }


def getArticles(url):

    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    for item in root:
        title = ""
        link = ""
        description = ""
        date = ""

        for article in item:
            if(article.tag == 'title'):
                title = article.text

            if (article.tag == 'link'):
                link = article.text

            if (article.tag == 'pubDate'):
                date = article.text
                date = datetime.strptime(date,'%a, %d %b %Y %H:%M:%S %z')

            if (article.tag == 'description'):
                description = article.text

        if(title != ""):
            if(date - timedelta(hours=24)):
                p = Paper(title, description, link, date)
                articles.append(p)
    return articles


# urls
igmchicago = 'https://www.igmchicago.org/wp-json/wp/v2/pages'
fivethirtyeight = 'https://feeds.megaphone.fm/ESP8794877317'
nasa_news = 'https://www.nasa.gov/rss/dyn/breaking_news.rss'
fred_news = 'https://news.research.stlouisfed.org/feed/'
mit_news = 'https://news.mit.edu/rss/feed'
mit_cs = 'http://www.eecs.mit.edu/rss.xml?'
mit_econ = 'https://news.mit.edu/rss/topic/economics'
mit_data = 'https://news.mit.edu/rss/topic/data-management-and-statistics'
mit_robotics = 'https://news.mit.edu/rss/topic/robotics'
econ_talk = 'https://feeds.simplecast.com/wgl4xEgL'
npr_news = 'https://feeds.npr.org/1001/rss.xml'
stanford_news = 'https://www.sup.org/rss/?feed=economics'
stanford_law = 'https://law.stanford.edu/news_type/sls-news/feed/'
stanford_soc = 'https://www.sup.org/rss/?feed=politics'

urls = [
    igmchicago,
    fivethirtyeight,
    nasa_news,
    fred_news,
    mit_news,
    mit_econ,
    mit_data,
    mit_robotics,
    econ_talk,
    npr_news,
    stanford_news
]

articles = []
for url in urls:
    try:
        articles = articles + getArticles(url)
    except:
        pass

print(len(articles))

