# EV Calculator & Betting Tracker App

A simple EV calculator and bet tracker. This was built following this [Flask app](https://flask.palletsprojects.com/en/stable/tutorial/) tutorial.[^1].

* Expected value and Kelly criterion calculation for singles and parlays, whether you have both sides available or not
* Bets are evaluated based on their quality and users can place them with one of the suggested amounts (based on their bankroll and unit size) or with a custom amount
* Recent bets can be viewed and set as either a win, loss, or not settled
* Profit and loss is adjusted based on the results of bets
* A simple line graph showing the user's bankroll is displayed on the home page of the app
* Users can select a data range for viewing bets
* The database can be backed up to an .sqlite file

![Unable to load GIF](https://github.com/kieranaston/personal-betting-app/blob/main/images/mainpage.gif)

## Table of Contents
- [How to navigate this project](#navigating-this-project)
- [How to install this project](#how-to-install-this-project)
- [Things I'd like to add](#features-id-like-to-add-in-the-future)

 ## Navigating this project

The file structure:

```
├── LICENSE
├── README.md
├── betting_app
│   ├── __init__.py
│   ├── backups.py
│   ├── bets.py
│   ├── db.py
│   ├── ev.py
│   ├── ev_calc.py
│   ├── graph.py
│   ├── schema.sql
│   ├── static
│   │   ├── bets.js
│   │   ├── ev.js
│   │   ├── graph.js
│   │   └── style.css
│   └── templates
│       ├── base.html
│       ├── bets.html
│       ├── ev.html
│       └── graph.html
├── requirements.txt
└── tests
    ├── conftest.py
    ├── data.sql
    ├── test_backup.py
    ├── test_bets.py
    ├── test_db.py
    ├── test_ev.py
    ├── test_ev_calc.py
    ├── test_factory.py
    └── test_graph.py
```

## How to install this project

Clone this repository: `git clone https://github.com/kieranaston/personal-betting-app.git`

Set up and activate a virtual environment in the project directory:

```
python3 -m venv .venv
. .venv/bin/activate
```

Make sure you have the latest version of pip installed: `python3 -m pip install --upgrade pip`

Install the project dependencies to the virtual environment you just set up: `pip install -r requirements.txt`

You can observe that the project dependencies are now installed with `pip list`

Initialize the database: `flask --app betting_app init-db`

There will now be a flaskr.sqlite file in the instance folder.

Run the Flask app using: `flask --app betting_app run`

Navigate to the url the Flask app is running on to access the homepage of the application.

## Features I'd like to add in the future

* API for retrieving odds from different sportsbooks
* Different visualization options for betting history
* User accounts

[^1]: Tutorial - Flask Documentation (3.0.x). (n.d.). https://flask.palletsprojects.com/en/stable/tutorial/
