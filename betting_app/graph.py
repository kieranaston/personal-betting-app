from flask import Blueprint, render_template, jsonify
from betting_app.db import get_db

graph_bp = Blueprint('graph', __name__)

@graph_bp.route('/')
def show_graph():
    # Renders the HTML page where the graph will be displayed
    return render_template('graph.html'), 200

@graph_bp.route('/graph', methods=['GET'])
def graph_data():
    # Fetches bankroll history from the database
    db = get_db()
    bankroll_history = db.execute(
        "SELECT date, new_bankroll FROM bankroll_history ORDER BY date"
    ).fetchall()

    # Formats data as a list of dictionaries for JSON response
    data = [
        {'date': entry['date'], 'new_bankroll': entry['new_bankroll'], 'message': 'Graph data retrieved successfully.'}
        for entry in bankroll_history
    ]
    return jsonify(data), 200