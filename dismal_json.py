# Imports
import csv
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

# Paper Object
class Paper:
    def __init__(self, title, description, link, date, source):
        self.title = title
        self.description = description
        self.link = link
        self.date = date
        self.source = source

    def __dict__(self):
        return {
            'Title': self.title,
            'Description': self.description,
            'Link': self.link,
            'Date': self.date,
            'Source': self.source
        }

urls = []

def getPaper(item):
    return 'Single Paper Object'

def getPapersFromUrl(url):
    return "List of Papers from a single URL"

def getPapersFromAllUrls():
    return "List of all Papers in reverse chronological order"

def createJson():
    return "Runs all of the above"

