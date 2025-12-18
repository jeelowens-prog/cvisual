import sqlite3
import os

# Paths to check for the database
db_paths = [
    'instance/cvisual.db',
    'cvisual.db',
    'instance/test.db',
    'test.db',
    'instance/database.db'
]

def migrate():
    found = False
    for path in db_paths:
        if os.path.exists(path):
            print(f"Found database at: {path}")
            try:
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                
                # Check if column exists
                cursor.execute("PRAGMA table_info(project)")
                columns = [info[1] for info in cursor.fetchall()]
                
                if 'live_link' not in columns:
                    print(f"Adding 'live_link' column to 'project' table in {path}...")
                    cursor.execute("ALTER TABLE project ADD COLUMN live_link TEXT")
                    conn.commit()
                    print("Migration successful!")
                else:
                    print(f"'live_link' column already exists in {path}.")
                
                conn.close()
                found = True
            except Exception as e:
                print(f"Error migrating {path}: {e}")
    
    if not found:
        print("No SQLite database files found to migrate. If you are using Neon/PostgreSQL, your table might need a manual ALTER TABLE project ADD COLUMN live_link TEXT; command.")

if __name__ == '__main__':
    migrate()
