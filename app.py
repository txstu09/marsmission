import pymongo
from flask import Flask, render_template, redirect

import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    #add variables from mongodb
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    news = scrape_mars.mars_news()
    image = scrape_mars.mars_image()
    weather = scrape_mars.mars_weather()
    facts = scrape_mars.mars_facts()
    hemispheres = scrape_mars.mars_hemispheres()

    db.news.insert_one(news)
    db.image.insert_one(image)
    db.weather.insert_one(weather)
    for fact in facts:
        db.facts.insert_one(fact)
    for hemisphere in hemispheres:
        db.hemispheres.insert_one(hemisphere)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)