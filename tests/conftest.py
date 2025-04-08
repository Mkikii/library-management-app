import os
import sys
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app, db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/library_test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-key-123'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'echo': True
    }
    # Add Flask-Caching configuration for tests
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    # Initialize the database
    from sqlalchemy_utils import create_database, database_exists, drop_database
    db_url = TestConfig.SQLALCHEMY_DATABASE_URI

    if database_exists(db_url):
        drop_database(db_url)
    create_database(db_url)

    app = create_app(TestConfig)

    with app.app_context():
        # Create tables
        db.create_all()
        yield app
        # Cleanup after all tests
        db.session.remove()
        db.drop_all()
        drop_database(db_url)

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Create a fresh database session for each test."""
    with app.app_context():
        # Clear data between tests
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        yield db.session

        # Rollback at the end of each test
        db.session.rollback()
