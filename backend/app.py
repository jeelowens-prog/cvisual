from flask import Flask, jsonify
from datetime import timedelta
import os
from dotenv import load_dotenv
from extensions import db, jwt, cors

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/cvisual_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
jwt.init_app(app)
cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

# Import models
from models import User, Project, BlogPost, Service, Testimonial, ContactMessage

# Import routes
from routes import projects, blog, services, testimonials, contact, auth

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(projects.bp, url_prefix='/api/projects')
app.register_blueprint(blog.bp, url_prefix='/api/blog')
app.register_blueprint(services.bp, url_prefix='/api/services')
app.register_blueprint(testimonials.bp, url_prefix='/api/testimonials')
app.register_blueprint(contact.bp, url_prefix='/api/contact')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'CVisual API is running'}), 200

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
