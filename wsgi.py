import sys
import os
from app import create_app

# Add project directory to Python path
project_path = '/home/MainaTim/library-management-app'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

application = create_app()
