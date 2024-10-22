from flask import (
    Blueprint, render_template, request, session, jsonify
)
from . import ev_calc
from betting_app.db import get_db
from datetime import datetime

ev_bp = Blueprint('ev', __name__, url_prefix='/ev')

@ev_bp.route('/place-bet', methods=['POST'])
def place_bet():
    try:
        bankroll = float(request.json.get('bankroll'))
        unit_size = float(request.json.get('unit_size'))
        your_odds = int(request.json.get('your_odds'))
        other_odds = request.json.get('other_odds')
        juice = session.get('juice')
        ev = session.get('value')
        kelly_units = session.get('kelly_units')

        if not ev or not juice or not kelly_units:
            return jsonify({'error': 'EV, juice, or Kelly units not found in session.'}), 400


        manual_units_placed = request.json.get('units_placed')
        if manual_units_placed:
            units_placed = float(manual_units_placed)
        else:
            kelly_percentage = request.json.get('kelly_percentage')
            units_placed = round(kelly_units[kelly_percentage], 2)

        bet_name = request.json.get('bet_name')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bets (date, bet_name, bankroll, unit_size, your_odds, other_odds, ev, units_placed, juice) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (date, bet_name, bankroll, unit_size, your_odds, other_odds, ev, units_placed, juice)
        )
        db.commit()

        bet_id = cursor.lastrowid

        cursor.execute(
            'INSERT INTO bankroll_history (bet_id, date, unit_size, change, new_bankroll) '
            'VALUES (?, ?, ?, ?, ?)',
            (bet_id, date, unit_size, 0, bankroll) 
        )
        db.commit()

        return jsonify({'bet_id': bet_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ev_bp.route('/ev-calculator', methods=['POST'])
def ev_calculator():
    bankroll = float(request.json.get('bankroll'))
    unit_size = float(request.json.get('unit_size'))
    your_odds = int(request.json.get('your_odds'))
    other_odds = request.json.get('other_odds')
    other_odds = ev_calc.split_odds(other_odds)

    juice = float(request.json.get('juice'))
    ev, juice, kelly_units = ev_calc.how_good(your_odds, other_odds, bankroll, unit_size, juice)
    session['value'] = ev
    session['juice'] = juice
    session['kelly_units'] = kelly_units
    return jsonify({'ev': ev, 'juice': juice, 'kelly_units': kelly_units})

@ev_bp.route('/get-bet/<int:bet_id>', methods=['GET'])
def get_bet(bet_id):
    try:
        db = get_db()
        bet = db.execute(
            'SELECT * FROM bets WHERE id = ?',
            (bet_id,)
        ).fetchone()

        if bet is None:
            return jsonify({'error': 'Bet not found'}), 404

        return jsonify({
            'bet_id': bet['id'],
            'bet_name': bet['bet_name'],
            'date': bet['date'],
            'bankroll': bet['bankroll'],
            'unit_size': bet['unit_size'],
            'your_odds': bet['your_odds'],
            'other_odds': bet['other_odds'],
            'ev': bet['ev'],
            'units_placed': bet['units_placed'],
            'juice': bet['juice']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ev_bp.route('/get-latest-bankroll', methods=['GET'])
def get_latest_bankroll():
    db = get_db()
    last_bankroll_entry = db.execute("SELECT new_bankroll FROM bankroll_history ORDER BY date DESC LIMIT 1").fetchone()
    latest_bankroll = last_bankroll_entry['new_bankroll'] if last_bankroll_entry else 100
    return jsonify({'latest_bankroll': latest_bankroll})

@ev_bp.route('/')
def index():
    return render_template('ev.html')