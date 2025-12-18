from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models import db, Admin, Project, ProjectImage, ProjectMetric, Service, ContactInquiry, NewsletterSubscriber
import cloudinary.uploader
import json

api = Blueprint('api', __name__)

# --- AUTH ---
@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    admin = Admin.query.filter_by(username=data.get('username')).first()
    if admin and check_password_hash(admin.password_hash, data.get('password')):
        access_token = create_access_token(identity=admin.username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

# --- PORTFOLIO ---
@api.route('/portfolio', methods=['GET'])
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    output = []
    for p in projects:
        project_data = {
            'id': p.id,
            'title': p.title,
            'category': p.category,
            'industry': p.industry,
            'date': p.date,
            'client': p.client,
            'duration': p.duration,
            'main_image': p.main_image,
            'challenge': p.challenge,
            'solution': p.solution,
            'testimonial': {
                'text': p.testimonial_text,
                'author': p.testimonial_author,
                'role': p.testimonial_role
            },
            'gallery': [img.image_url for img in p.gallery],
            'metrics': [{'label': m.label, 'value': m.value} for m in p.metrics],
            'live_link': p.live_link
        }
        output.append(project_data)
    return jsonify(output)

@api.route('/portfolio', methods=['POST'])
@jwt_required()
def add_project():
    try:
        # Multi-part form data to handle image upload
        title = request.form.get('title')
        category = request.form.get('category')
        industry = request.form.get('industry', '')
        date = request.form.get('date', '')
        client = request.form.get('client', '')
        duration = request.form.get('duration', '')
        challenge = request.form.get('challenge', '')
        solution = request.form.get('solution', '')
        testimonial_text = request.form.get('testimonial_text', '')
        testimonial_author = request.form.get('testimonial_author', '')
        testimonial_role = request.form.get('testimonial_role', '')
        live_link = request.form.get('live_link', '')
        
        # Handle main image upload to Cloudinary
        file_to_upload = request.files.get('main_image')
        main_image_url = ""
        if file_to_upload:
            try:
                upload_result = cloudinary.uploader.upload(file_to_upload, folder="cvisual/portfolio")
                main_image_url = upload_result.get('secure_url')
            except Exception as e:
                return jsonify({"error": f"Cloudinary upload failed: {str(e)}"}), 500

        new_project = Project(
            title=title, category=category, industry=industry, date=date,
            client=client, duration=duration, challenge=challenge, 
            solution=solution, main_image=main_image_url,
            testimonial_text=testimonial_text, testimonial_author=testimonial_author,
            testimonial_role=testimonial_role, live_link=live_link
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        # Handle gallery images
        gallery_files = request.files.getlist('gallery')
        for f in gallery_files:
            if f:
                try:
                    up_res = cloudinary.uploader.upload(f, folder=f"cvisual/portfolio/{new_project.id}")
                    img = ProjectImage(project_id=new_project.id, image_url=up_res.get('secure_url'))
                    db.session.add(img)
                except Exception as e:
                    print(f"Gallery image upload failed: {e}")
                
        # Handle metrics (expected as JSON string in form data)
        metrics_str = request.form.get('metrics', '[]')
        try:
            metrics = json.loads(metrics_str)
            for m in metrics:
                metric = ProjectMetric(project_id=new_project.id, label=m.get('label'), value=m.get('value'))
                db.session.add(metric)
        except json.JSONDecodeError:
            print("Invalid metrics JSON, skipping")
            
        db.session.commit()
        return jsonify({"message": "Project added successfully", "id": new_project.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/portfolio/<int:id>', methods=['PUT'])
@jwt_required()
def update_project(id):
    try:
        project = Project.query.get_or_404(id)
        
        project.title = request.form.get('title', project.title)
        project.category = request.form.get('category', project.category)
        project.industry = request.form.get('industry', project.industry)
        project.date = request.form.get('date', project.date)
        project.client = request.form.get('client', project.client)
        project.duration = request.form.get('duration', project.duration)
        project.challenge = request.form.get('challenge', project.challenge)
        project.solution = request.form.get('solution', project.solution)
        project.testimonial_text = request.form.get('testimonial_text', project.testimonial_text)
        project.testimonial_author = request.form.get('testimonial_author', project.testimonial_author)
        project.testimonial_role = request.form.get('testimonial_role', project.testimonial_role)
        project.live_link = request.form.get('live_link', project.live_link)
        
        # Handle main image update if a new file is provided
        file_to_upload = request.files.get('main_image')
        if file_to_upload:
            try:
                upload_result = cloudinary.uploader.upload(file_to_upload, folder="cvisual/portfolio")
                project.main_image = upload_result.get('secure_url')
            except Exception as e:
                return jsonify({"error": f"Cloudinary upload failed: {str(e)}"}), 500

        db.session.commit()
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/portfolio/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_project(id):
    try:
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- CONTACT ---
@api.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    new_inquiry = ContactInquiry(
        first_name=data.get('firstName'),
        last_name=data.get('lastName'),
        email=data.get('email'),
        phone=data.get('phone'),
        company=data.get('company'),
        service_type=data.get('service'),
        budget=data.get('budget'),
        timeline=data.get('timeline'),
        message=data.get('message'),
        contact_method=data.get('contactMethod')
    )
    db.session.add(new_inquiry)
    db.session.commit()
    return jsonify({"message": "Inquiry submitted"}), 201

@api.route('/inquiries', methods=['GET'])
@jwt_required()
def get_inquiries():
    inquiries = ContactInquiry.query.order_by(ContactInquiry.created_at.desc()).all()
    return jsonify([{
        'id': i.id,
        'name': f"{i.first_name} {i.last_name}",
        'email': i.email,
        'service': i.service_type,
        'status': i.status,
        'date': i.created_at.isoformat()
    } for i in inquiries])

# --- SERVICES ---
@api.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'delay': s.delay,
        'price': s.starting_price,
        'roi': s.roi,
        'icon': s.icon_type,
        'anchor': s.details_anchor
    } for s in services])

@api.route('/services/<int:id>', methods=['PUT'])
@jwt_required()
def update_service(id):
    data = request.get_json()
    service = Service.query.get_or_404(id)
    
    service.name = data.get('name', service.name)
    service.delay = data.get('delay', service.delay)
    service.starting_price = data.get('price', service.starting_price)
    service.roi = data.get('roi', service.roi)
    
    db.session.commit()
    return jsonify({"message": "Service updated"})
@api.route('/newsletter', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    if NewsletterSubscriber.query.filter_by(email=email).first():
        return jsonify({"message": "Already subscribed"}), 200
    
    new_sub = NewsletterSubscriber(email=email)
    db.session.add(new_sub)
    db.session.commit()
    return jsonify({"message": "Subscribed successfully"}), 201
