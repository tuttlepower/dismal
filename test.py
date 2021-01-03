# lets start with getting data
import Paper
import csv
import requests
import xml.etree.ElementTree as ET

url = "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"

r = requests.get(url)

for line in r.text.split():
    if ('thumbnails/image' in line):
        line = line[5:-1]
        print(line)

    if('description' in line):
        print(line)
    
