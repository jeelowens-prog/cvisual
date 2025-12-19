import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_migrate import Migrate
from models import db, Admin, Project, ProjectImage, ProjectMetric, Service, ContactInquiry, NewsletterSubscriber
from routes import api
import cloudinary

load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Render provides 'postgres://', but SQLAlchemy 1.4+ requires 'postgresql://'
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///cvisual.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(api, url_prefix='/api')

# Debug environment loading
print(f"DEBUG: Current Working Directory: {os.getcwd()}")
print(f"DEBUG: .env file exists: {os.path.exists('.env')}")

# Cloudinary configuration
# Try separate variables first
cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')
cloudinary_url = os.getenv('CLOUDINARY_URL')

if cloudinary_url:
    print("DEBUG: CLOUDINARY_URL found, using it.")
    cloudinary.config(cloudinary_url = cloudinary_url)
elif all([cloud_name, api_key, api_secret]):
    print("DEBUG: Individual Cloudinary variables found, using them.")
    cloudinary.config(
      cloud_name = cloud_name,
      api_key = api_key,
      api_secret = api_secret
    )
else:
    print("WARNING: No valid Cloudinary configuration found in .env!")
    print(f"DEBUG: CLOUDINARY_CLOUD_NAME: {bool(cloud_name)}")
    print(f"DEBUG: CLOUDINARY_API_KEY: {bool(api_key)}")
    print(f"DEBUG: CLOUDINARY_API_SECRET: {bool(api_secret)}")

# Routes will be added here

@app.route('/')
def home():
    return jsonify({"message": "CVisual API is running"})

if __name__ == '__main__':
    app.run(debug=True)
