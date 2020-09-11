# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    mars_info = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scraping():

    # Run the scrape function
    mars_info = scrape_mars.scrape()

    # Update the Mongo database
    mongo.db.mars.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)