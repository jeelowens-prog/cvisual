import os
import sys

# Ensure current directory is in path
sys.path.append(os.getcwd())

from app import app, db
from sqlalchemy import inspect
from flask_migrate import upgrade, stamp

def setup_db():
    print("--- Starting Database Setup ---")
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Found tables: {tables}")
            
            if 'alembic_version' in tables:
                print("Alembic version table exists. Running upgrade...")
                upgrade()
            elif 'admin' in tables or 'project' in tables:
                print("Existing business tables found but no migrations history. Stamping to 'head'...")
                # Force stamp to head to tell Alembic we are already at the latest version
                stamp(revision='head')
                print("Database stamped as 'head'. Running upgrade to confirm...")
                upgrade()
            else:
                print("Empty database found. Running initial upgrade...")
                upgrade()
            print("--- Database setup complete ---")
        except Exception as e:
            print(f"!!! Error during database setup: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    setup_db()
