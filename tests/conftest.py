import pytest
from flask import Flask
from models import db as original_db
#
@pytest.fixture(scope='session') 
def test_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testing-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    original_db.init_app(app)
    with app.app_context():
        original_db.create_all()
        yield app
        original_db.session.remove()
@pytest.fixture(scope='function')
def db_session(test_app):
    with test_app.app_context():
        yield original_db.session
        original_db.session.rollback() 