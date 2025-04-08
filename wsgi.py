import sys
import os

# Add project directory to Python path
project_path = '/home/yourusername/library-management-app'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from app import create_app
application = create_app()
