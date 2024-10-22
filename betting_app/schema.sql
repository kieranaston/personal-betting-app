DROP TABLE IF EXISTS bets;
DROP TABLE IF EXISTS bankroll_history;

CREATE TABLE bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    bet_name TEXT NOT NULL,
    bankroll REAL NOT NULL,
    unit_size REAL NOT NULL,
    your_odds INTEGER NOT NULL,
    other_odds TEXT NOT NULL,
    ev REAL NOT NULL,
    units_placed REAL NOT NULL,
    juice REAL NOT NULL,
    outcome TEXT,
    profit_loss REAL
);

CREATE TABLE bankroll_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bet_id INTEGER,              -- Link to the specific bet causing this change
    date TEXT NOT NULL,          -- Date of the change
    unit_size REAL NOT NULL,     -- Unit size at the time of the bet
    change REAL NOT NULL,        -- Change in bankroll in dollars (profit/loss * unit_size)
    new_bankroll REAL NOT NULL,  -- New bankroll after applying the change
    FOREIGN KEY (bet_id) REFERENCES bets(id) ON DELETE CASCADE
);