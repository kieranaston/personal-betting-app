import sqlite3

import pytest
from betting_app.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

        # below block was added
        result = db.execute('SELECT 1').fetchone()
        assert result is not None

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)