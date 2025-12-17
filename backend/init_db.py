#!/usr/bin/env python
"""Initialize database with default admin user"""

from app import app
from extensions import db
from models import User
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize database and create default admin"""
    with app.app_context():
        print("\n🔧 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!\n")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("👤 Creating default admin user...")
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@cvisual.ht')
            admin_password = os.getenv('ADMIN_PASSWORD', 'changeme123')
            
            admin = User(
                username=admin_username,
                email=admin_email,
                full_name='CVisual Admin',
                role='admin'
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Admin user created successfully!")
            print(f"   Username: {admin_username}")
            print(f"   Email: {admin_email}")
            print(f"   Password: {admin_password}")
            print(f"\n⚠️  IMPORTANT: Change the default password after first login!\n")
        else:
            print("✅ Admin user already exists.\n")

if __name__ == '__main__':
    init_database()
