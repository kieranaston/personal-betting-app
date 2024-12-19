from flask import session

def test_place_bet_valid_input(client):
    with client as c:
        with client.session_transaction() as session:
        # Set session variables
            session['value'] = 0.3
            session['kelly_units'] = {0.25: 0.3}
            session['juice'] = 0.06
        response = c.post('/ev/place-bet', json={'bankroll': '100.00', 'unit_size': 1.0, 'your_odds': 150, 'other_odds': '150, 160', 'units_placed': 3,
                                                 'kelly_percentage': '0.25', 'bet_name': 'Test Bet'})
        assert response.status_code == 200
        assert b'Bet placed successfully.' in response.data

def test_place_bet_invalid_input(client):
    with client as c:
        with client.session_transaction() as session:
            session['value'] = 0.3
            session['kelly_units'] = {0.25: 0.3}
            session['juice'] = 0.06
        response = c.post('/ev/place-bet', json={'bankroll': '11.12456', 'unit_size': 1.0, 'your_odds': 150, 'other_odds': '150, 160', 'units_placed': 3,
                                                 'kelly_percentage': '0.25', 'bet_name': 'Test Bet'})
        assert response.status_code == 400
        assert b'Bankroll must be a monetary value.' in response.data

        response = c.post('/ev/place-bet', json={'bankroll': '11', 'unit_size': -1.0, 'your_odds': 150, 'other_odds': '150, 160', 'units_placed': 3,
                                                 'kelly_percentage': '0.25', 'bet_name': 'Test Bet'})
        assert response.status_code == 400
        assert b'Unit size must be positive' in response.data

        response = c.post('/ev/place-bet', json={'bankroll': '11', 'unit_size': 1.0, 'your_odds': 0, 'other_odds': '150, 160', 'units_placed': 3,
                                                 'kelly_percentage': '0.25', 'bet_name': 'Test Bet'})
        assert response.status_code == 400
        assert b'Your odds must be American format.' in response.data

        response = c.post('/ev/place-bet', json={'bankroll': '11', 'unit_size': 1.0, 'your_odds': 150, 'other_odds': '150, 160', 'units_placed': -3,
                                                 'kelly_percentage': '0.25', 'bet_name': 'Test Bet'})
        assert response.status_code == 400
        assert b'Units placed must be positive.' in response.data

def test_calculate_ev_valid_input(client):
    with client as c:
        response = c.post('/ev/ev-calculator', json={'bankroll': '100.00', 'unit_size': 1.0, 'your_odds': 150, 'other_odds': '150, 160', 'juice': 0.06})
        assert response.status_code == 200
        assert b'EV calculated successfully.' in response.data

def test_calculate_ev_invalid(client):
    with client as c:
        response = c.post('/ev/ev-calculator', json={'bankroll': '100.0080', 'unit_size': 1.0, 'your_odds': 150, 'other_odds': '150, 160', 'juice': 0.06})
        assert response.status_code == 400
        assert b'Bankroll must be a monetary value.' in response.data

        response = c.post('/ev/ev-calculator', json={'bankroll': '100.00', 'unit_size': -1.0, 'your_odds': 150, 'other_odds': '150, 160', 'juice': 0.06})
        assert response.status_code == 400
        assert b'Unit size must be positive.' in response.data

        response = c.post('/ev/ev-calculator', json={'bankroll': '100.00', 'unit_size': 1.0, 'your_odds': 0, 'other_odds': '150, 160', 'juice': 0.06})
        assert response.status_code == 400
        assert b'Your odds must be American format.' in response.data

        response = c.post('/ev/ev-calculator', json={'bankroll': '100.00', 'unit_size': 1.0, 'your_odds': 150, 'other_odds': '150, 160', 'juice': -0.06})
        assert response.status_code == 400
        assert b'Juice must be a percentage.' in response.data

def test_get_bet_valid(client):
    with client as c:
        response = c.get('/ev/get-bet/1')
        assert response.status_code == 200
        assert b'Bet retrieved successfully' in response.data

def test_get_bet_invalid(client):
    with client as c:
        response = c.get('/ev/get-bet/999')
        assert response.status_code == 404
        assert b'Bet not found' in response.data

def test_get_latest_bankroll(client):
    with client as c:
        response = c.get('ev/get-latest-bankroll')
        assert response.status_code == 200
        assert b'Latest bankroll retrieved successfully.' in response.data

def test_get_latest_unit_size(client):
    with client as c:
        response = c.get('ev/get-latest-unit-size')
        assert response.status_code == 200
        assert b'Latest unit size retrieved successfully.' in response.data

def test_index_route(client):
    # Send a GET request to the index route
    response = client.get('/')

    # Assert the status code is 200
    assert response.status_code == 200

    # Assert the response contains content from the rendered template
    assert b'EV Calculator' in response.data  # Replace with actual content from ev.html