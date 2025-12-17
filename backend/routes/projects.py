from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Project
from datetime import datetime
from utils.cloudinary_helper import upload_image, delete_image

bp = Blueprint('projects', __name__)

@bp.route('/', methods=['GET'])
def get_projects():
    """Get all projects (public)"""
    try:
        status = request.args.get('status', 'published')
        category = request.args.get('category')
        featured = request.args.get('featured')
        
        query = Project.query
        
        if status:
            query = query.filter_by(status=status)
        
        if category:
            query = query.filter_by(category=category)
        
        if featured:
            query = query.filter_by(featured=True)
        
        projects = query.order_by(Project.order_position, Project.created_at.desc()).all()
        
        return jsonify({
            'projects': [project.to_dict() for project in projects],
            'total': len(projects)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get single project by ID"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({'project': project.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    """Create new project (Admin only)"""
    try:
        data = request.get_json()
        
        project = Project(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            image_url=data.get('image_url'),
            thumbnail_url=data.get('thumbnail_url'),
            client_name=data.get('client_name'),
            project_date=datetime.fromisoformat(data.get('project_date')) if data.get('project_date') else None,
            tags=data.get('tags', []),
            featured=data.get('featured', False),
            status=data.get('status', 'draft'),
            order_position=data.get('order_position', 0)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update project (Admin only)"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            project.title = data['title']
        if 'description' in data:
            project.description = data['description']
        if 'category' in data:
            project.category = data['category']
        if 'image_url' in data:
            project.image_url = data['image_url']
        if 'thumbnail_url' in data:
            project.thumbnail_url = data['thumbnail_url']
        if 'client_name' in data:
            project.client_name = data['client_name']
        if 'project_date' in data:
            project.project_date = datetime.fromisoformat(data['project_date']) if data['project_date'] else None
        if 'tags' in data:
            project.tags = data['tags']
        if 'featured' in data:
            project.featured = data['featured']
        if 'status' in data:
            project.status = data['status']
        if 'order_position' in data:
            project.order_position = data['order_position']
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete project (Admin only)"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_project_image():
    """Upload project image to Cloudinary"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        folder = request.form.get('folder', 'projects')
        
        result = upload_image(file, folder)
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'url': result['secure_url'],
            'public_id': result['public_id']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
