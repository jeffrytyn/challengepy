user_data=[]

def new_user(username, year, school, favorites):
    user = {
        'username': username ,
        'year': year ,
        'school': school ,
        'favorites': [favorites]
    }
    return user


