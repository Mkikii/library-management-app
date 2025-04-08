import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_test_db():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    # Drop test database if it exists
    cur.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'library_test_db'
        AND pid <> pg_backend_pid();
    """)
    cur.execute("DROP DATABASE IF EXISTS library_test_db")

    # Create test database
    cur.execute("CREATE DATABASE library_test_db")

    cur.close()
    conn.close()

if __name__ == '__main__':
    init_test_db()
