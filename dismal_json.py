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
            'Date': self.date}


url_list = {
    'FiveThirtyEight': 'https://feeds.megaphone.fm/ESP8794877317',
    'NASA': 'https://www.nasa.gov/rss/dyn/breaking_news.rss',
    'FRED': 'https://news.research.stlouisfed.org/feed/',
    'MIT News': 'https://news.mit.edu/rss/feed',
    'MIT Econ': 'https://news.mit.edu/rss/topic/economics',
    'MIT Data': 'https://news.mit.edu/rss/topic/data-management-and-statistics',
    'MIT Robotics': 'https://news.mit.edu/rss/topic/robotics',
    'EconTalk': 'https://feeds.simplecast.com/wgl4xEgL',
    'NPR': 'https://feeds.npr.org/1001/rss.xml',
    'Stanford News': 'https://www.sup.org/rss/?feed=economics'
}


def getPaper(item, url):
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
            date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z').date()

        if (article.tag == 'description'):
            description = article.text

    if(title != "" and link != "" and description != "" and date != "" and date > datetime.now().date()-timedelta(days=7)):
        return Paper(title, description, link, date)
    else:
       return None


def getPapersFromUrl(url):
    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    for item in root:
        articles.append(getPaper(item, url))
    return articles


def getPapersFromAllUrls():
    return "List of all Papers in reverse chronological order"


def createJson(article):
    f = open("dismal-json.js", "a")
    [f.write(article.__dict__()) for article in articles]
    f.close()


# articles = getPapersFromUrl(url_list['MIT Econ'])
# articles = [article for article in articles if article is not None]
# articles.sort(key=lambda x: x.date, reverse=True)

# for a in articles:
#     print('title', a.title)
#     print('description', a.description)
#     print('link', a.link)
#     print('date', a.date)

# print([article.__dict__() for article in articles])
# createJson(articles)

print('Fin')
