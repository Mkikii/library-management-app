import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # Cache Configuration
    CACHE_TYPE = 'simple'  # Change to Redis for better performance
    CACHE_DEFAULT_TIMEOUT = 300
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_KEY_PREFIX = 'library_'

    # Compression Configuration
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json']

    # Database Connection Pool
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'echo': True  # Add this to see SQL queries during development
    }

    # Query timeout for slow query logging
    DATABASE_QUERY_TIMEOUT = 0.5  # in seconds
