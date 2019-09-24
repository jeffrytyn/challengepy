# Penn Labs Server Challenge
Remember to **document your work** in this `README.md` file! Feel free to delete these installation instructions in your fork of this repository.

## Installation
1. Fork + clone this repository. 
2. `cd` into the cloned repository.
3. Install `pipenv`
  * `brew install pipenv` if you're on a Mac.
  * `pip install --user --upgrade pipenv` for most other machines.
4. Install packages using `pipenv install`.

## Developing
1. Use `pipenv run index.py` to run the project.
2. Follow the instructions [here](https://www.notion.so/pennlabs/Server-Challenge-Fall-19-480abf1871fc4a8d9600154816726343).
3. Document your work in the `README.md` file.

## Submitting
Submit a link to your git repository to [this form](https://airtable.com/shrqdIzlLgiRFzEWh) by 11:59pm on Monday, September 23rd.

## Installing Additional Packages
To install additional packages run `pipenv install <package_name>` within the cloned repository.

## Club/User objects
I created two .py files for the Club and User object, `club_groups.py` and `club_users.py`. The Club object contains the attributes `name`, `tags`, `descr`, which corresponds to a description of the club, and `likes`, which corresponds to how many people have favorited the club. The User object has the attributes `username`, `password`, which is hashed, `school`, `year`, and `favorites`, which lists the user's favorite clubs. The classes are used when creating new clubs or registering new users. A user named `jen` is created in `club_users.py`.

## JSON files
The data scraped from the website is in `club_data.json`. When new clubs are created, that data is added to this file as well. Similarly, the data for users is added to `club_users.json`. If you open `club_users.json`, you will see that `jen` and her information is available. For each new user that is registered, their information is added to `club_users.json`.

## Routes
#### /api/clubs
With a `GET`request, the data for all the clubs currently available is returned in JSON format. A `POST` request allows you to create a club from the parameters `name`, `tags`, and `descr`, which will be added to the `all_clubs` dictionary and dumped into `club_data.json`.

#### /api/user/(username)
This checks if some user is currently logged in. If no user is logged in, it returns a message. If a user is logged in, their information (excluding their password) is returned in JSON format.

#### /api/register
This allows people to register as new users. Based on the information they provide, a new `User` is created. If this new `User` has a username that is already taken, it will return a message. Otherwise, this new user will be added to the `all_users` dictionary and then dumped into `club_users.json`.

#### /api/signin
This allows people to sign in. Based on the information they provide, if they have an account and they provide the correct password corresponding to their account, their username is added to `session`, indicating they are signed in. Otherwise, a message is returned indicating they do not have an account or their password is incorrect.

#### /api/signout
This allows people to sign out. Based on the information they provide, their username is removed from `session` if they are currently logged in. Otherwise, a message is returned indicating they are not currently logged and hence cannot log out.

## Future Features
- Transition data to SQLite or MySQL for more heavy duty data storage and access.
- Implement stylized front end to allow users to input data.
- Add more features such as linking club interest forms to Club objects and implementing a notification feature who users who have favorited a certain club. 
- Rigorous debugging tests.
