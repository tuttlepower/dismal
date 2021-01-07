# lets start with getting data
import Paper
import csv
import requests
import xml.etree.ElementTree as ET

def getArxivFeed(url):

    r = requests.get(url)
    root = ET.fromstring(r.text)
    articles = []

    for x in root:
        title = ""
        link = ""
        description = ""

        for y in x:
            if('title' in y.tag):
                line = y.text.split(". ", 1)
                line = line[0]
                title = line

            if('link' in y.tag):
                link = y.text

            if('description' in y.tag):
                line = y.text[3:-5]
                line = line.replace('<p>','')
                line = line.replace('</p>','')
                description = line

        if(title != ""):
            p = Paper.Paper(title, description, link)
            articles.append(p)
                
    return articles

url = 'http://export.arxiv.org/rss/econ'
# url = 'http://export.arxiv.org/rss/q-fin'


r = requests.get(url)
root = ET.fromstring(r.text)

# for child in root:
#     for node in child:
#         print(child.tag + 
#         "--" + node.tag)

url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=10'
# r = requests.get(url)
# root = ET.fromstring(r.text)
# print(root.tag)

articles = getArxivFeed(url)

for x in articles:
    print(x.title)