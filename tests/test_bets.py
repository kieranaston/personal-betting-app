import pytest
from datetime import datetime, timedelta

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

def test_update_bet_status_success(client):
    # Prepare test data in the database
    test_bet_id = 1
    new_status = 'won'

    response = client.post(f'/bets/update-bet-status/{test_bet_id}', data={'status': new_status})

    assert response.status_code == 200
    assert b'Bet status updated successfully' in response.data

def test_update_bet_status_invalid_status(client):
    test_bet_id = 1
    invalid_status = ''  # Empty status, which is invalid

    response = client.post(f'/bets/update-bet-status/{test_bet_id}', data={'status': invalid_status})

    assert response.status_code == 400
    assert b'Invalid status' in response.data