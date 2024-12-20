import sqlite3
import pytest
import json
import os
from datetime import datetime
from flask import g
from betting_app import create_app
from unittest.mock import patch


def test_backup_db(client):
    response = client.post('/backup-db')

    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'message' in data
    assert 'Database backup successful!' in data['message']

    current_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    expected_backup_file_name = f'./backups/betting_app_backup_{current_date_time}.sqlite'
    assert os.path.isfile(expected_backup_file_name)

    if os.path.isfile(expected_backup_file_name):
        os.remove(expected_backup_file_name)
