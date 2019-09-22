import json

class User:
    def __init__(self, name, year, school, favorites):
        self.name = name
        self.year = year
        self.school = school
        self.favorites = favorites

    def user_json(self):
        user_json = {
            'username': self.name ,
            'year': self.year ,
            'school': self.school ,
            'favorites': self.favorites
        }
        return user_json

user_data={}

Jen = User('jen',2023,'SEAS',["PennLabs",'CSS'])
user_data['jen'] = Jen.user_json()

with open('club_users.json','w') as userfile:
    json.dump(user_data, userfile, indent = 1)

