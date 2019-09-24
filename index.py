from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from club_users import *
from club_groups import *
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
import os
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club_users.db'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)


#If I had more time, I would try to store club and user data with SQLAlchemy instead of JSON.

#class Club(db.Model): 
#    name = db.Column(db.String, unique = True, primary_key = True, nullable = False)
#    tags = db.Column(db.String)
#    descr = db.Column(db.String)
#    favoriters = db.relationship('User', backref = 'best_club', lazy = True)
#    favorites = db.Column(db.Integer, default = 0)

#    def __repr__(self):
#        return f"Club('{self.name}', '{self.tags}', '{self.descr}','{self.favorites}')"

#class User(db.Model):
#    username = db.Column(db.String, unique = True, primary_key = True, nullable = False)
#    year = db.Column(db.Integer, nullable = False)
#    school = db.Column(db.String, nullable = False)
#    best = db.Column(db.String, db.ForeignKey('club.name'), nullable = True)

#    def __repr__(self):
#        return f"User('{self.username}', '{self.year}', '{self.school}','{self.best}')"

#for club_html in get_clubs(soupify(get_clubs_html())):
#        name = get_club_name(club_html)
#        tag = get_club_tags(club_html)
#        descr = get_club_description(club_html) 
#        new_club = Club(name = name, tags = tag, descr = descr, favorites = 0)
#        db.session.add(new_club)
#        db.session.commit()



"""
Open club_data file to load into a dictionary to be manipulated 
"""
with open('club_data.json') as clubfile:
    all_clubs = json.load(clubfile)
clubfile.close()


"""
Open club_users file to load into dictionary to be manipulated
"""
with open('club_users.json') as clubfile:
    all_users = json.load(clubfile)
clubfile.close()


@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."


"""
GET: Retrieve the information for all the clubs in JSON format
POST: Add new club object and its information to to all_clubs dictionary.
      If the new club has a name that already exists, it will return an alert.
"""
@app.route('/api/clubs', methods = ['GET', 'POST'])
def api_clubs():
    if request.method == "GET":
        with open('club_data.json','w') as clubfile:
            json.dump(all_clubs, clubfile, indent = 4)
        clubfile.close()
        return jsonify(all_clubs)
    else:
        name = request.form['name']
        tags = list(request.form['tag'])
        descr = request.form['descr']
        if not(name in all_clubs.keys()):
            new_club = Club(name, tags, descr, likes = 0)
            all_clubs[name] = new_club.club_json()
            with open('club_data.json', 'w') as clubfile:
                json.dump(all_clubs, clubfile)
            clubfile.close()
        else: 
            return "That club already exists."


"""
Return safe information for a certain user in JSON format. If that user is not logged in
all_users, it will return a message.
"""
@app.route('/api/user/<username>', methods = ['GET'])
def return_user_profile(username):
    if 'user' in session:
        with open('club_users.json','w') as clubfile:
            json.dump(all_users, clubfile, indent = 4)
        clubfile.close()
        return jsonify(all_users[username].safe_data())
    else:
        return "Not logged in."


"""
Creates a new user with all the attributes filled. This user's password is hashed
and his/her data is addded to the all_users dictionary and stored in the club_users
JSON file.
"""
@app.route('/api/register', methods = ['GET','POST'])
def register_new_user():
    username = request.form['username']
    password = request.form['password']
    year = request.form['year']
    school = request.form['school']
    favorites = list(request.form['favorites'])
    new_user = User(username, password, year, school, favorites).encode_pw()
    if not(username in all_users.keys()):
        all_users[username] = new_user.user_json()
        with open('club_users.json','w') as clubfile:
            json.dump(all_users, clubfile, indent = 4)
        clubfile.close()
        return "New user successfully added!"
    else:
        return "That user already exists!"

"""
Route that enables users to login. Checks to see if user exists.
Checks to see if entered password matches hashed password already 
stored, and if so, adds a session key and value.
"""
@app.route('/api/signin', methods = ['GET','POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not(username in all_users.keys()):
        return "This user does not exist!"
    else:
        hashed = all_users[username][password]
        if bcrypt.checkpw(password,hashed):
            session['user'] = username
            return "Successfully signed in."
        else:
            return "Incorrect password. Try again."

"""
When a user attempts to logout, this deletes the user entry
in the session dictionary, allowing a new user to sign in.
"""
@app.route('/api/signout', methods = ['GET','POST'])
def logout():
    if 'user' in session:
        session.pop('user',None)
        return "Successfully logged out."
    else:
        return "No user is logged in."    

"""
Adds a certain club to a user's favorite attribute and increases the club's favorite count. 
If the club is already a user's favorite, the club will be removed and its favorite count 
will be reduced. The user must be logged in for the request to be processed.
"""
@app.route('/api/favorite', methods = ["POST"])
def mark_favorite():
    if 'user' in session:
        user = session['user']
        club = request.form["club"]
        if club in all_users[user]["favorites"]:
            all_users[user]["favorites"] = all_users[user]["favorites"].remove(club)
            if all_clubs[club]["likes"] - 1 < 0:  
                all_clubs[club]["likes"] = 0
            else:
                all_clubs[club]["likes"] -= 1
            return "Club removed from favorites list."
        else:
            all_users[user]["favorites"].append(club)
            all_clubs[club]["likes"] += 1
            return "Club added to favorites list."
    else:
        return "You must login to favorite clubs."

if __name__ == '__main__':
    app.run()
