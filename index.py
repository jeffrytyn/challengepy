from flask import Flask, request
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
app = Flask(__name__)

class Club:
    def __init__(self, name, tags, descr):
        self.name = name
        self.tags = tags
        self.descr = descr

class User:
    def _init_(self, name, year, school, favorite):
        self.name = name
        self.year = year
        self.school = school
        self.favorite = favorite

@app.route('/')
def main():
    soupify(get_clubs_html())
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."





if __name__ == '__main__':
    app.run()
