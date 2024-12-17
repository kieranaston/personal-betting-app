-- Example data.sql with default date handling
INSERT INTO bets (id, bet_name, bankroll, unit_size, your_odds, other_odds, ev, units_placed, juice, outcome, profit_loss, date)
VALUES
(1, 'Test  Bet 1', 100, 1.00, 150, 'avg(-120, -130)', 2.4, 1.25, 0.06, 'won', 2.3, CURRENT_DATE),
(2, 'Test Bet 2', 110, 1.00, 173, 'avg(120, 130)', 2.7, 1.05, 0.06, 'lost', -1.05, CURRENT_DATE),
(3, 'Test Bet 3', 123, 1.3, 180, 'avg(120, 130)', 2.9, 1.15, 0.065, 'pending', -1.35, CURRENT_DATE),
(4, 'Test Bet 4', 121, 1.7, 130, 'avg(120, 130)', 2.1, 1.35, 0.075, 'pending', NULL, CURRENT_DATE);

INSERT INTO bankroll_history (id, bet_id, date, unit_size, change, new_bankroll)
VALUES
(11, 1, '2024-12-17', 1.25, 2.3, 102.3),
(12, 2, '2024-12-18', 1.05, -1.05, 108.95),
(13, 3, '2024-12-16', 1.45, -1.095, 108.97),
(14, 4, '2024-12-16', 1.49, -1.035, 140.97);