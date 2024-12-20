def test_index_route(client):

    response = client.get('/')

    assert response.status_code == 200

    assert b'Bankroll Graph' in response.data 

def test_graph_data(client):
    with client as c:
        response = c.get('/graph')
        assert response.status_code == 200
        assert b'Graph data retrieved successfully.' in response.data