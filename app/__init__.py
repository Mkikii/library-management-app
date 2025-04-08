from flask import Flask
from flask_migrate import Migrate
from flask_caching import Cache
from flask_compress import Compress
from config import Config
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
compress = Compress()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    compress.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

    return app
