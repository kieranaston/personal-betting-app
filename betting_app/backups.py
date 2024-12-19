import shutil
import os
from flask import Blueprint, jsonify
from datetime import datetime

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/backup-db', methods=['POST'])
def backup_db():
    backup_dir = './backups'
    os.makedirs(backup_dir, exist_ok=True)
    current_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file_name = f'backups/betting_app_backup_{current_date_time}.sqlite'
    shutil.copyfile('instance/betting_app.sqlite', backup_file_name)
    return jsonify({'message': f'Database backup successful! Backup file: {backup_file_name}'}), 200
