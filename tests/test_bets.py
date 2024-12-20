import pytest
from datetime import datetime, timedelta
from betting_app.db import get_db
import betting_app.ev_calc as ev_calc

def test_view_bets_valid_range(client):
    start_date = '2024-12-11'
    end_date = '2024-12-18'

    response = client.get(f'/bets/view-bets?start_date={start_date}&end_date={end_date}')
    assert response.status_code == 200
    assert b'Test Bet 1' in response.data or b'Test Bet 2' in response.data
    assert b'won' in response.data or b'lost' in response.data

def test_view_bets_missing_start_date(client):
    response = client.get('/bets/view-bets')
    assert response.status_code == 200
    assert b'Test Bet 1' in response.data or b'Test Bet 2' in response.data

def test_view_bets_invalid_date_range(client):
    start_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    response = client.get(f'/bets/view-bets?start_date={start_date}&end_date={end_date}')

    assert response.status_code == 200
    assert b'Start date cannot be after the end date.' in response.data

def test_view_bets_missing_end_date(client):
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    response = client.get(f'/bets/view-bets?start_date={start_date}')

    assert response.status_code == 200
    assert b'Test Bet 1' in response.data or b'Test Bet 2' in response.data

def test_view_bets_no_results(client):
    response = client.get(f'/bets/view-bets?start_date=2025-01-01&end_date=2025-01-31')

    assert response.status_code == 200
    assert b'No bets found for the specified date range.' in response.data

def test_update_bet_status_success(client, app):
    test_bet_id = 1
    new_status = 'won'

    response = client.post(f'/bets/update-bet-status/{test_bet_id}', data={'status': new_status})

    assert response.status_code == 200
    assert b'Bet status updated successfully' in response.data

    with app.app_context():
        db = get_db()
        outcome = db.execute('SELECT outcome FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert outcome['outcome'] == new_status

def test_update_bet_status_invalid_status(client, app):
    test_bet_id = 1
    invalid_status = ''

    response = client.post(f'/bets/update-bet-status/{test_bet_id}', data={'status': invalid_status})

    assert response.status_code == 400
    assert b'Invalid status' in response.data

    with app.app_context():
        db = get_db()
        outcome = db.execute('SELECT outcome FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert outcome['outcome'] != invalid_status

def test_update_bet_status_non_existent_bet(client, app):
    non_existent_bet_id = 999

    response = client.post(f'/bets/update-bet-status/{non_existent_bet_id}', data={'status': 'won'})

    assert response.status_code == 400
    assert b'Bet not found' in response.data

def test_update_profit_loss_winning_bet(client, app):
    test_bet_id = 1
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Profit/Loss updated successfully'

    with app.app_context():
        db = get_db()
        bet = db.execute('SELECT * FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert bet is not None
        odds = ev_calc.american_to_decimal(bet['your_odds'])
        expected_profit_loss = (bet['units_placed'] * odds) - bet['units_placed']
        expected_profit_loss = round(expected_profit_loss, 2)
        assert bet['profit_loss'] == expected_profit_loss

def test_update_profit_loss_invalid_bet_outcome(client):

    test_bet_id = 3
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')

    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['error_message'] == 'Invalid bet outcome'

def test_update_profit_loss_non_existent_bet(client):

    non_existent_bet_id = 999
    response = client.post(f'/bets/update-profit-loss/{non_existent_bet_id}')

    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data['error_message'] == 'Bet not found'

def test_update_profit_loss_lost_bet(client, app):
    test_bet_id = 2
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Profit/Loss updated successfully'

    with app.app_context():
        db = get_db()
        bet = db.execute('SELECT * FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert bet is not None
        expected_profit_loss = -bet['units_placed']
        assert bet['profit_loss'] == expected_profit_loss

def test_update_profit_loss_not_settled(client, app):
    test_bet_id = 5
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Profit/Loss updated successfully'
    with app.app_context():
        db = get_db()
        bet = db.execute('SELECT * FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert bet is not None
        expected_profit_loss = 0
        assert bet['profit_loss'] == expected_profit_loss


def test_update_bankroll_success(client, app):
    test_bet_id = 1

    response = client.post(f'/bets/update-bankroll/{test_bet_id}')

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Bankroll updated successfully'

    with app.app_context():
        db = get_db()
        bet = db.execute(
            "SELECT * FROM bets WHERE id = ? ORDER BY date DESC LIMIT 1",
            (test_bet_id,)
        ).fetchone()
        bankroll_entry = db.execute(
            "SELECT * FROM bankroll_history WHERE bet_id = ? ORDER BY date DESC LIMIT 1",
            (test_bet_id,)
        ).fetchone()

        assert bankroll_entry is not None
        assert bankroll_entry['change'] == bet['profit_loss'] * bet['unit_size']

def test_update_bankroll_no_profit_loss(client, app):
    test_bet_id = 4

    response = client.post(f'/bets/update-bankroll/{test_bet_id}')

    with app.app_context():
        db = get_db()
        bankroll_entry = db.execute(
            "SELECT new_bankroll FROM bankroll_history WHERE bet_id = ? ORDER BY date DESC LIMIT 1",
            (test_bet_id,)
        ).fetchone()
        previous = bankroll_entry['new_bankroll']

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'No profit/loss to update for this bet.'

    with app.app_context():
        db = get_db()
        bankroll_entry = db.execute(
            "SELECT new_bankroll FROM bankroll_history WHERE bet_id = ? ORDER BY date DESC LIMIT 1",
            (test_bet_id,)
        ).fetchone()

        assert bankroll_entry is not None
        assert bankroll_entry['new_bankroll'] == previous

def test_update_bankroll_bet_not_found(client):
    non_existent_bet_id = 999 

    response = client.post(f'/bets/update-bankroll/{non_existent_bet_id}')

    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data['error_message'] == 'Bet not found'