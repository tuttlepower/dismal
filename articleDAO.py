import xml.etree.ElementTree as ET
import requests
import csv
import Paper


def getArticles(url):

    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []
    root = root[0]
    for item in root:
        title = ""
        link = ""
        description = ""

        for article in item:
            if(article.tag == 'title'):
                title = article.text

            if (article.tag == 'link'):
                link = article.text

            if (article.tag == 'description'):
                description = article.text

        if(title != ""):
            p = Paper.Paper(title, description, link)
            articles.append(p)
    return articles

def getNasa():

    images = []

    url = "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"

    r = requests.get(url)

    for line in r.text.split():
        if ('thumbnails/image' in line):
            line = line[5:-1]
            images.append(line)
    
    return images