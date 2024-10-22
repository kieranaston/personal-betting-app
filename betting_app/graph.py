from flask import Blueprint, render_template, jsonify
from betting_app.db import get_db

graph_bp = Blueprint('graph', __name__)

# Route to render the bankroll graph page
@graph_bp.route('/')
def show_graph():
    return render_template('graph.html')

# Route to serve the bankroll data
@graph_bp.route('/graph', methods=['GET'])
def graph_data():
    db = get_db()
    # Fetch bankroll history from the database
    bankroll_history = db.execute("SELECT date, new_bankroll, bet_id FROM bankroll_history ORDER BY date").fetchall()

    # Prepare data to send to the frontend
    data = []
    for entry in bankroll_history:
        bet = db.execute("SELECT bet_name FROM bets WHERE id = ?", (entry['bet_id'],)).fetchone()
        data.append({
            'date': entry['date'],
            'new_bankroll': entry['new_bankroll'],
            'bet_name': bet['bet_name'] if bet else "Unknown Bet"
        })

    return jsonify(data)