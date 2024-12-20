# EV Calculator & Betting Tracker App

A simple EV calculator and bet tracker.

* Expected value and Kelly criterion calculation for singles and parlays, whether you have both sides available or not
* Bets are evaluated based on their quality and users can place them with one of the suggested amounts (based on their bankroll and unit size) or with a custom amount
* Recent bets can be viewed and set as either a win, loss, or not settled
* Profit and loss is adjusted based on the results of bets
* A simple line graph showing the user's bankroll is displayed on the home page of the app
* Users can select a data range for viewing bets
* The database can be backed up to an .sqlite file

## Table of Contents
- [How to navigate this project](#how-to-navigate-this-project)
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
├── pyproject.toml
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

Install the project in the virtual environment: `pip install -e .`

You can observe that the project is now installed with pip list.

Initialize the database: `flask --app flaskr init-db`

There will now be a flaskr.sqlite file in the instance folder.

Run the Flask app using: `flask run`

Navigate to the url provided in a browser to access the homepage of the application.

## Features I'd like to add in the future

* API for retrieving odds from different sportsbooks
* Different visualization options for betting history
* User accounts

[^1]: Tutorial - Flask Documentation (3.0.x). (n.d.). https://flask.palletsprojects.com/en/stable/tutorial/
