import pandas as pd

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
    browser = Browser('chrome', headless=True)
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

def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df = df.rename(columns={0:'description',1:'value'})
    facts = df.to_dict('records')
    return(facts)

def mars_hemispheres():
    browser = Browser('chrome', headless=True)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []
    for x in range(4):
        css_link = "div.collapsible.results > div:nth-child("+str(x+1)+") > div > a"
        browser.find_by_css(css_link).click()
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        image_url = downloads.find('a')['href']
        title_text = soup.find('h2', class_='title').text
        title_split = title_text.split()
        del title_split[-1]
        title = " ".join(title_split)
        hemisphere_image_urls.append({'image_url':image_url,'title':title})
        browser.back()
    return(hemisphere_image_urls)    