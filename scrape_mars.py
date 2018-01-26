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
    return(news)

def mars_image():
    browser = Browser('chrome', headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_id('full_image')
    html = browser.html
    soup = bs(html, 'html.parser')
    img_tag = soup.find_all('img', class_='fancybox-image')
    img_link = f"https://www.jpl.nasa.gov{img_tag[0]['src']}"
    image = {'image_link':img_link}
    return(image)

def mars_weather():
    browser = Browser('chrome', headless=True)
    url = 'https://twitter.com/MarsWxReport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    tweets = soup.find_all('p', class_='tweet-text')
    for tweet in tweets:
        tweet_split = tweet.text.split()
        if tweet_split[0] == 'Sol':
            weather_tweet = tweet.text
            break
    weather = {'current_weather':weather_tweet}
    return(weather)