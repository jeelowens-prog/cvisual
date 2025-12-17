from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='admin')  # admin, super_admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # web, photography, social-media, design, content
    image_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    client_name = db.Column(db.String(150))
    project_date = db.Column(db.Date)
    tags = db.Column(db.JSON)  # ["e-commerce", "responsive", "modern"]
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='published')  # draft, published, archived
    order_position = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url,
            'client_name': self.client_name,
            'project_date': self.project_date.isoformat() if self.project_date else None,
            'tags': self.tags,
            'featured': self.featured,
            'status': self.status,
            'order_position': self.order_position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text)
    featured_image = db.Column(db.String(500))
    author = db.Column(db.String(100))
    category = db.Column(db.String(100))
    tags = db.Column(db.JSON)
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    published_at = db.Column(db.DateTime)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'content': self.content,
            'featured_image': self.featured_image,
            'author': self.author,
            'category': self.category,
            'tags': self.tags,
            'status': self.status,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'views_count': self.views_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))  # Icon name or SVG
    image_url = db.Column(db.String(500))
    features = db.Column(db.JSON)  # ["Feature 1", "Feature 2"]
    pricing = db.Column(db.String(100))
    order_position = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'image_url': self.image_url,
            'features': self.features,
            'pricing': self.pricing,
            'order_position': self.order_position,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    client_name = db.Column(db.String(150), nullable=False)
    client_position = db.Column(db.String(150))
    client_company = db.Column(db.String(150))
    client_avatar = db.Column(db.String(500))
    testimonial_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)  # 1-5 stars
    project_type = db.Column(db.String(100))
    metrics = db.Column(db.JSON)  # {"sales": "+250%", "engagement": "+300%"}
    is_featured = db.Column(db.Boolean, default=False)
    order_position = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_position': self.client_position,
            'client_company': self.client_company,
            'client_avatar': self.client_avatar,
            'testimonial_text': self.testimonial_text,
            'rating': self.rating,
            'project_type': self.project_type,
            'metrics': self.metrics,
            'is_featured': self.is_featured,
            'order_position': self.order_position,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, replied, archived
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
