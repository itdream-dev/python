from app.ivysaur_app import create_app
from flask.ext.migrate import upgrade, Manager, Migrate
from lib.registry import get_registry


_app = None


def get_app():
    global _app
    return _app


def set_app(app):
    global _app
    _app = app


def create_test_environment():
    app = create_app('test')
    Manager(app)
    db = get_registry()['DB']
    Migrate(app, db)
    with app.app_context():
        upgrade()
    set_app(app)
    return app
