import os
import sys

# Ensure current directory is in path
sys.path.append(os.getcwd())

from app import app, db
from sqlalchemy import inspect
from flask_migrate import upgrade, stamp, current

def setup_db():
    print("\n--- DATABASE SETUP START ---")
    with app.app_context():
        try:
            # Use inspector to get all tables across all schemas (primarily public)
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Existing tables detected: {tables}")
            
            # Check for migrations history
            has_alembic = 'alembic_version' in tables
            # Check for core business tables
            has_core_tables = any(t in tables for t in ['admin', 'project', 'service', 'contact_inquiry'])
            
            if has_alembic:
                current_rev = current()
                print(f"Current Alembic revision: {current_rev}")
                if current_rev is None and has_core_tables:
                    print("Alembic history exists but no revision set, and core tables present. Stamping to head...")
                    stamp(revision='head')
                else:
                    print("Proceeding with standard upgrade...")
                    upgrade()
            elif has_core_tables:
                print("CRITICAL: Core tables already exist but no migration history found.")
                print("This database was likely initialized previously without migrations.")
                print("Stamping database as 'head' to skip initial creation steps...")
                # Stamp tells Alembic 'we are already at the latest version'
                # Use current head from the migrations folder
                stamp(revision='head')
                print("Database marked as 'head'. Success.")
                # No need to upgrade right after stamping if we stamped to head
            else:
                print("Empty database detected. Running initial migrations...")
                upgrade()
                
            print("--- DATABASE SETUP COMPLETE ---\n")
            
        except Exception as e:
            print(f"\n!!! DATABASE SETUP ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    setup_db()
