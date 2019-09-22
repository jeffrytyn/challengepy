from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from club_users import *
from club_groups import *
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club_users.db'
db = SQLAlchemy(app)

"""
If I had more time, I would try to store club and user data with SQLAlchemy instead of JSON.

class Club(db.Model): 
    name = db.Column(db.String, unique = True, primary_key = True, nullable = False)
    tags = db.Column(db.String)
    descr = db.Column(db.String)
    favoriters = db.relationship('User', backref = 'best_club', lazy = True)
    favorites = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"Club('{self.name}', '{self.tags}', '{self.descr}','{self.favorites}')"

class User(db.Model):
    username = db.Column(db.String, unique = True, primary_key = True, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    school = db.Column(db.String, nullable = False)
    best = db.Column(db.String, db.ForeignKey('club.name'), nullable = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.year}', '{self.school}','{self.best}')"

for club_html in get_clubs(soupify(get_clubs_html())):
        name = get_club_name(club_html)
        tag = get_club_tags(club_html)
        descr = get_club_description(club_html) 
        new_club = Club(name = name, tags = tag, descr = descr, favorites = 0)
        db.session.add(new_club)
        db.session.commit()
"""

with open('club_data.json') as clubfile:
    all_clubs = json.load(clubfile)
    clubfile.close()

with open('club_users.json') as clubfile:
    all_users = json.load(clubfile)
    clubfile.close()


@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods = ['GET', 'POST'])
def api_clubs():
    if request.method == "GET":
        with open('club_data.json','w') as clubfile:
            json.dump(all_clubs, clubfile, indent = 1)
        clubfile.close()
        return jsonify(all_clubs)
    else:
        name = request.form['name']
        tags = [request.form['tag']]
        descr = request.form['descr']
        if len(all_clubs[name]) == 0:
            new_club = Club(name, tags, descr, likes = 0)
            all_clubs[name] = new_club
        else: 
            return "That club already exists."

@app.route('/api/user/<username>', methods = ['GET'])
def return_user_profile(username):
    if len(all_users[username]) > 0:
        return jsonify(all_users[username])
    else:
        return "No such user exists."

@app.route('/api/favorite', methods = ["POST"])
def mark_favorite():
    user = request.form['name']
    club = request.form["club"]
    if club in all_users[user]["favorites"]:
        all_users[user]["favorites"] = all_users[user]["favorites"].remove(club)
        all_clubs[club]["likes"] -= 1
        return "Club removed from favorites list."
    else:
        all_users[user]["favorites"].append(club)
        all_clubs[club]["likes"] += 1
        return "Club added to favorites list."
        
if __name__ == '__main__':
    app.run()
