import os
import sys

# Ensure current directory is in path
sys.path.append(os.getcwd())

from app import app, db
from sqlalchemy import inspect
from flask_migrate import upgrade, stamp

def setup_db():
    print("Checking database state...")
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'alembic_version' in tables:
                print("Alembic version table exists. Running upgrade...")
                upgrade()
            elif 'admin' in tables:
                print("Existing tables found (e.g., 'admin') but no migrations history. Stamping as head...")
                stamp()
                print("Database stamped. Running upgrade...")
                upgrade()
            else:
                print("Empty database found. Running initial upgrade...")
                upgrade()
            print("Database setup complete.")
        except Exception as e:
            print(f"Error during database setup: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup_db()
