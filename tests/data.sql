-- Example data.sql with default date handling
INSERT INTO bets (id, bet_name, bankroll, unit_size, your_odds, other_odds, ev, units_placed, juice, outcome, profit_loss, date)
VALUES
(1, 'Test  Bet 1', 100, 1.00, 150, 'avg(-120, -130)', 2.4, 1.25, 0.06, 'Won', 2.3, CURRENT_DATE),
(2, 'Test Bet 2', 110, 1.00, 173, 'avg(120, 130)', 2.7, 1.05, 0.06, 'Lost', -1.05, CURRENT_DATE);

INSERT INTO bankroll_history (id, bet_id, date, unit_size, change, new_bankroll)
VALUES
(11, 1, '2024-12-17', 1.25, 2.3, 102.3),
(12, 2, '2024-12-18', 1.05, -1.05, 108.95);