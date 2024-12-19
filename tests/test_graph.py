def test_index_route(client):
    # Send a GET request to the index route
    response = client.get('/')

    # Assert the status code is 200
    assert response.status_code == 200

    # Assert the response contains content from the rendered template
    assert b'Bankroll Graph' in response.data  # Replace with actual content from ev.html

def test_graph_data(client):
    with client as c:
        response = c.get('/graph')
        assert response.status_code == 200
        assert b'Graph data retrieved successfully.' in response.data