from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_compress import Compress
from config import Config

# Initialize extensions first without app context
db = SQLAlchemy(session_options={"expire_on_commit": False})
migrate = Migrate()
cache = Cache()
compress = Compress()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    cache.init_app(app)
    compress.init_app(app)

    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    return app
