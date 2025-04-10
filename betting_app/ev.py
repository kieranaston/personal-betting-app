from flask import (
    Blueprint, render_template, request, session, jsonify
)
from . import ev_calc
from betting_app.db import get_db
from datetime import datetime
import re

ev_bp = Blueprint('ev', __name__, url_prefix='/ev')

@ev_bp.route('/place-bet', methods=['POST'])
def place_bet():
    bankroll = float(request.json.get('bankroll'))
    if bankroll <= 0 or len(str(bankroll).split('.')[1]) > 2:
        return jsonify({'error': 'Bankroll must be a monetary value.'}), 400
    unit_size = float(request.json.get('unit_size'))
    if unit_size < 0:
            return jsonify({'error': 'Unit size must be positive.'}), 400
    your_odds = int(request.json.get('your_odds'))
    if your_odds == 0:
            return jsonify({'error': 'Your odds must be American format.'}), 400
    other_odds = request.json.get('other_odds')

    manual_units_placed = request.json.get('units_placed')

    juice = session.get('juice')
    ev = session.get('value')
    kelly_units = session.get('kelly_units')

    if manual_units_placed:
        if manual_units_placed <= 0:
             return jsonify({'error': 'Units placed must be positive.'}), 400
        units_placed = float(manual_units_placed)
        units_placed = round(units_placed)
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
    return jsonify({'bet_id': bet_id, 'message': 'Bet placed successfully.'}), 200

@ev_bp.route('/ev-calculator', methods=['POST'])
def ev_calculator():
    bankroll = float(request.json.get('bankroll'))
    if bankroll <= 0 or len(str(bankroll).split('.')[1]) > 2:
        return jsonify({'error': 'Bankroll must be a monetary value.'}), 400
    unit_size = float(request.json.get('unit_size'))
    if unit_size < 0:
            return jsonify({'error': 'Unit size must be positive.'}), 400
    your_odds = int(request.json.get('your_odds'))
    if your_odds == 0:
            return jsonify({'error': 'Your odds must be American format.'}), 400

    other_odds = request.json.get('other_odds')
    other_odds = ev_calc.split_odds(other_odds)

    juice = float(request.json.get('juice'))
    if juice < 0 or juice > 1:
         return jsonify({'error': 'Juice must be a percentage.'}), 400

    ev, juice, kelly_units = ev_calc.how_good(your_odds, other_odds, bankroll, unit_size, juice)

    session['value'] = round(ev, 4)
    session['juice'] = round(juice, 3)
    session['kelly_units'] = kelly_units

    return jsonify({'ev': ev, 'juice': juice, 'kelly_units': kelly_units, 'message': 'EV calculated successfully.'}), 200

@ev_bp.route('/get-bet/<int:bet_id>', methods=['GET'])
def get_bet(bet_id):
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
        'juice': bet['juice'],
        'message': 'Bet retrieved successfully'}), 200

@ev_bp.route('/get-latest-bankroll', methods=['GET'])
def get_latest_bankroll():
    db = get_db()
    last_bankroll_entry = db.execute("SELECT new_bankroll FROM bankroll_history ORDER BY date DESC LIMIT 1").fetchone()
    latest_bankroll = last_bankroll_entry['new_bankroll'] if last_bankroll_entry else 100
    latest_bankroll = round(latest_bankroll, 2)
    return jsonify({'latest_bankroll': latest_bankroll, 'message': 'Latest bankroll retrieved successfully.'}), 200

@ev_bp.route('/get-latest-unit-size', methods=['GET'])
def get_latest_unit_size():
    db = get_db()
    latest_unit_size = db.execute("SELECT unit_size FROM bankroll_history ORDER BY date DESC LIMIT 1").fetchone()
    latest_unit_size = latest_unit_size['unit_size'] if latest_unit_size else 1.00
    return jsonify({'latest_unit_size': latest_unit_size, 'message': 'Latest unit size retrieved successfully.'}), 200

@ev_bp.route('/')
def index():
    return render_template('ev.html'), 200
