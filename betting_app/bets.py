from flask import (
    Blueprint, render_template, jsonify, request
)
from betting_app.db import get_db
from datetime import datetime, timedelta
from . import ev_calc

bets_bp = Blueprint('bets', __name__, url_prefix='/bets')

@bets_bp.route('/view-bets', methods=['GET'])
def view_bets():
    db = get_db()
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    query = """
        SELECT * FROM bets
        WHERE DATE(date) BETWEEN ? AND ?
        ORDER BY date DESC
    """
    bets = db.execute(query, (start_date, end_date)).fetchall()

    return render_template('bets.html', bets=bets, start_date=start_date, end_date=end_date)

@bets_bp.route('/update-bet-status/<int:bet_id>', methods=['POST'])
def update_bet_status(bet_id):
    db = get_db()
    new_status = request.form.get('status')
    if not new_status:
        return jsonify({'error': 'Invalid status'}), 400
    query = "UPDATE bets SET outcome = ? WHERE id = ?"
    db.execute(query, (new_status, bet_id))
    db.commit()
    return jsonify({'message': 'Bet status updated successfully'}), 200

@bets_bp.route('/update-profit-loss/<int:bet_id>', methods=['POST'])
def update_profit_loss(bet_id):
    db = get_db()
    bet = db.execute("SELECT * FROM bets WHERE id = ?", (bet_id,)).fetchone()
    if bet['outcome'] == 'won':
        odds = ev_calc.american_to_decimal(bet['your_odds'])
        profit_loss = (bet['units_placed'] * odds) - bet['units_placed']
    elif bet['outcome'] == 'lost':
        profit_loss = -bet['units_placed']
    else:
        profit_loss = 0
    profit_loss = round(profit_loss, 2)
    db.execute("UPDATE bets SET profit_loss = ? WHERE id = ?", (profit_loss, bet_id))
    db.commit()

    return jsonify({'message': 'Profit/Loss updated successfully', 'profit_loss': profit_loss}), 200

@bets_bp.route('/update-bankroll/<int:bet_id>', methods=['POST'])
def update_bankroll(bet_id):
    db = get_db()

    bet = db.execute("SELECT * FROM bets WHERE id = ?", (bet_id,)).fetchone()
    new_change = bet['profit_loss'] * bet['unit_size'] if bet['profit_loss'] is not None else 0
    previous_entry = db.execute("SELECT * FROM bankroll_history WHERE bet_id = ? ORDER BY date DESC LIMIT 1", (bet_id,)).fetchone()
    last_bankroll_entry = db.execute("SELECT new_bankroll FROM bankroll_history ORDER BY date DESC LIMIT 1").fetchone()
    starting_bankroll = last_bankroll_entry['new_bankroll'] if last_bankroll_entry else bet['bankroll']
    if previous_entry:
        starting_bankroll -= previous_entry['change']
    new_bankroll = starting_bankroll + new_change
    db.execute("""
        INSERT INTO bankroll_history (bet_id, date, unit_size, change, new_bankroll)
        VALUES (?, ?, ?, ?, ?)
    """, (bet_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bet['unit_size'], new_change, new_bankroll))

    db.commit()

    return jsonify({'message': 'Bankroll updated successfully', 'new_bankroll': new_bankroll}), 200