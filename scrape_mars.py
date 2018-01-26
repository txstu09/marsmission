import pandas as pd
import pymongo
import flask

from splinter import Browser
from bs4 import BeautifulSoup as bs

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = mars_db

def mars_news():
    browser = Browser('chrome', headless=True)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    result_title = soup.find('div', class_='content_title')
    result_teaser = soup.find('div', class_='article_teaser_body')
    news_title = result_title.text
    news_teaser = result_teaser.text
    news = {'title':news_title,'lede':news_teaser}
    return (news)

def mars_image():