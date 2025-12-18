import os
import sys
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Add the current directory to sys.path so we can import app and models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Admin

load_dotenv()

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database tables created.")

        # Create default admin if not exists
        username = os.getenv('ADMIN_USERNAME', 'admin')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if not Admin.query.filter_by(username=username).first():
            hashed_pw = generate_password_hash(password)
            default_admin = Admin(username=username, password_hash=hashed_pw)
            db.session.add(default_admin)
            db.session.commit()
            print(f"Default admin created: {username}")
        else:
            print(f"Admin {username} already exists.")

if __name__ == "__main__":
    init_db()
