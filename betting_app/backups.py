import shutil
from flask import Blueprint, jsonify
from datetime import datetime

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/backup-db', methods=['POST'])
def backup_db():
    try:
        # Get the current date in the format YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Construct the backup file name with the date appended
        backup_file_name = f'backups/flaskr_backup_{current_date}.sqlite'
        # Copy the database to the new backup file
        shutil.copyfile('instance/betting_app.sqlite', backup_file_name)
        return jsonify({'message': f'Database backup successful! Backup file: {backup_file_name}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500