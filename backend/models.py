from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., "Site Web", "Photographie"
    industry = db.Column(db.String(50)) # e.g., "ecommerce", "restaurant"
    date = db.Column(db.String(50)) # e.g., "Janvier 2025"
    client = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    main_image = db.Column(db.String(255)) # Cloudinary URL
    challenge = db.Column(db.Text)
    solution = db.Column(db.Text)
    testimonial_text = db.Column(db.Text)
    testimonial_author = db.Column(db.String(100))
    testimonial_role = db.Column(db.String(100))
    live_link = db.Column(db.String(255)) # Optional link to live site
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship for gallery
    gallery = db.relationship('ProjectImage', backref='project', lazy=True, cascade="all, delete-orphan")
    # Relationship for metrics
    metrics = db.relationship('ProjectMetric', backref='project', lazy=True, cascade="all, delete-orphan")

class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class ProjectMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    label = db.Column(db.String(100), nullable=False) # e.g., "Augmentation des Ventes"
    value = db.Column(db.String(50), nullable=False) # e.g., "+250%"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    delay = db.Column(db.String(50))
    starting_price = db.Column(db.String(50))
    roi = db.Column(db.String(50))
    icon_type = db.Column(db.String(50)) # For the SVG icon selection
    details_anchor = db.Column(db.String(50)) # e.g., "#website-creation"

class ContactInquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100))
    service_type = db.Column(db.String(50))
    budget = db.Column(db.String(50))
    timeline = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    contact_method = db.Column(db.String(20)) # email, phone, whatsapp
    status = db.Column(db.String(20), default='pending') # pending, contacted, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
