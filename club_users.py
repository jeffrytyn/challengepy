import json
import bcrypt

class User:
    """
    Used to create a User
    """
    def __init__(self, username, password, year, school, favorites):
        self.username = username
        self.password = password.encode('utf-8')
        self.year = year
        self.school = school
        self.favorites = favorites
    """
    Used to convert User object to be added to JSON file
    """
    def user_json(self):
        user_json = {
            'username': self.username ,
            'password': self.password,
            'year': self.year ,
            'school': self.school ,
            'favorites': self.favorites
        }
        return user_json

    """
    Hashes the user's password as to not be easily seen. Changes the user's password attribute
    """
    def encode_pw(self):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(self.password,salt).decode('utf-8')
        self.password = hashed_pw
        return self

    """
    Returns the data for a user excluding their password
    """
    def safe_data(self):
        copy = dict(self.user_json())
        del copy['password']
        return copy            


"""
Creating 'jen'
"""
user_data={}
Jen = User('jen','Password',2023,'SEAS',["PennLabs",'CSS']).encode_pw()
user_data['jen'] = Jen.user_json()

with open('club_users.json','w') as userfile:
    json.dump(user_data, userfile, indent = 4)
userfile.close()