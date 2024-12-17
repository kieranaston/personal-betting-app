import os
import tempfile
import shutil

import pytest
from betting_app import create_app
from betting_app.db import get_db, init_db

BACKUP_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'backups', 'betting_app_backup_2024-12-13.sqlite')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    shutil.copyfile(BACKUP_FILE_PATH, db_path)

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()