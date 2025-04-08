from setuptools import setup, find_packages

setup(
    name="library-management-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask>=2.3.3',
        'Flask-SQLAlchemy>=3.1.1',
        'Flask-Migrate>=4.0.5',
        'psycopg2>=2.9.1',
    ],
)
