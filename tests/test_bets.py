import pytest
from datetime import datetime, timedelta
from betting_app.db import get_db
import betting_app.ev_calc as ev_calc

def test_view_bets_valid_range(client):
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    response = client.get(f'/bets/view-bets?start_date={start_date}&end_date={end_date}')

    assert response.status_code == 200
    assert b'Test Bet 1' in response.data or b'Test Bet 2' in response.data
    assert b'Won' in response.data or b'Lost' in response.data

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
    # Prepare test data in the database
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
    invalid_status = ''  # Empty status, which is invalid

    response = client.post(f'/bets/update-bet-status/{test_bet_id}', data={'status': invalid_status})

    assert response.status_code == 400
    assert b'Invalid status' in response.data

    with app.app_context():
        db = get_db()
        outcome = db.execute('SELECT outcome FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert outcome['outcome'] != invalid_status

def test_update_bet_status_non_existent_bet(client, app):
    non_existent_bet_id = 999  # Assuming this ID doesn't exist in the test data

    response = client.post(f'/bets/update-bet-status/{non_existent_bet_id}', data={'status': 'won'})

    assert response.status_code == 400
    assert b'Bet not found' in response.data

def test_update_profit_loss_winning_bet(client, app):
    # Prepare test data: A bet with 'won' outcome and specific odds and units_placed
    test_bet_id = 1
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Profit/Loss updated successfully'

    # Verify the profit/loss value in the database
    with app.app_context():
        db = get_db()
        bet = db.execute('SELECT * FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert bet is not None
        odds = ev_calc.american_to_decimal(bet['your_odds'])
        expected_profit_loss = (bet['units_placed'] * odds) - bet['units_placed']
        expected_profit_loss = round(expected_profit_loss, 2)
        assert bet['profit_loss'] == expected_profit_loss

def test_update_profit_loss_invalid_bet_outcome(client):

    # Prepare test data: A bet with an invalid outcome
    test_bet_id = 3  # Use an existing bet
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')  # Invalid outcome

    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['error_message'] == 'Invalid bet outcome'

def test_update_profit_loss_non_existent_bet(client):
    # Non-existent bet ID
    non_existent_bet_id = 999
    response = client.post(f'/bets/update-profit-loss/{non_existent_bet_id}')

    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data['error_message'] == 'Bet not found'

def test_update_profit_loss_lost_bet(client, app):
    test_bet_id = 2  # Use an existing bet with 'lost' outcome
    response = client.post(f'/bets/update-profit-loss/{test_bet_id}')

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Profit/Loss updated successfully'

    # Verify the profit/loss in the database
    with app.app_context():
        db = get_db()
        bet = db.execute('SELECT * FROM bets WHERE id = ?', (test_bet_id,)).fetchone()
        assert bet is not None
        expected_profit_loss = -bet['units_placed']
        assert bet['profit_loss'] == expected_profit_loss