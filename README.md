# EV Calculator & Betting Tracker App

A minimalistic EV calculator and bet tracker. 

* Expected value and Kelly criterion calculation for singles and parlays, whether you have both sides available or not
* Bets are evaluated based on their quality and users can place them with one of the suggested unit sizes (based on their bankroll) or with a custom unit size
* Recent bets can be viewed and set as either a win, loss, or not settled
* Profit and loss is adjusted based on the results of bets
* A simple line graph showing the user's bankroll is displayed on the home page of the app

## Table of Contents
- [How to navigate this project](#how-to-navigate-this-project)
- [Why?](#why-i-built-this-project)
- [If I had more time what would I change](#if-i-had-more-time-what-would-i-change)

 ## How to navigate this project
 
The file structure:

```
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
└── requirements.txt
```

## Why I built this project

I am not big on sports betting, however, I was interested in experienting with particular betting strategies and how much success I might have with them. Many tools for this sort of thing are available online, but are often behind a paywall and/or superfluous and complicated to use. 

For my application build and database implementation I followed [this Flask tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)[^1].

I thought it would be a good exercise to better understand EV betting and the Kelly criterion to implement it myself in my own web app. Additionally, I wanted a web app to keep track of all my bets as well as my bankroll over time so that I could easily see how good a bet is, what I should put on it, and what my bankroll is looking like all in one convenient place. 

One thing I did not like about many online tools is that you as a user are often having to trust the tools to provide you with profitable bets. I prefer my own personal system because it provides a balance between choosing the bets or sports that you feel confident betting, and from those bets choosing only the ones that give you the best edge. 

## If I had more time what would I change?

I have several ideas for things I would like to add to my web app in the future. First and foremost, I would like to begin using an odds API both for retrieving the best lines, as well as retrieving lines from other sportsbooks for bets I am interested in. Right now I do all of this manually (luckily I am able to access this informatioxn all in one place for the most part, however, the manual odds entry into my app does take time), and I believe it would make my system much more efficient to achieve this with an API instead. 

Another thing I want to add is more visualizations of my betting statistics. I intend to include a page solely for visualizations, and include things such as a calendar of the last month with graded coloring for each day indicating how much in the green or how much in the red I was for that given day, along with the dollar amount of loss/profit on that day. I'm sure there are many other insights I could add in addition to that idea. 

[^1]: Tutorial - Flask Documentation (3.0.x). (n.d.). https://flask.palletsprojects.com/en/stable/tutorial/ 
