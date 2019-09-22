import json
user_data=[]

def new_user(username, year, school, favorites):
    user = {
        'username': username ,
        'year': year ,
        'school': school ,
        'favorites': favorites
    }
    return user

user_data.append(new_user('jen','2023','SEAS',['PennLabs','CSS']))

with open('club_users.json','w') as userfile:
    json.dump(user_data, userfile, indent = 1)

