import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'betting_app.sqlite'),
        SESSION_COOKIE_SAMESITE = 'Lax',
        SESSION_COOKIE_SECURE = False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import ev
    app.register_blueprint(ev.ev_bp)

    from . import bets
    app.register_blueprint(bets.bets_bp)

    from . import graph
    app.register_blueprint(graph.graph_bp)

    from . import backups
    app.register_blueprint(backups.backup_bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app