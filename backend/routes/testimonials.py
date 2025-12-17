from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Testimonial
from datetime import datetime

bp = Blueprint('testimonials', __name__)

@bp.route('/', methods=['GET'])
def get_testimonials():
    """Get all testimonials (public)"""
    try:
        is_active = request.args.get('is_active')
        is_featured = request.args.get('is_featured')
        limit = request.args.get('limit', type=int)
        
        query = Testimonial.query
        
        # Public access only shows active testimonials
        if not request.headers.get('Authorization'):
            query = query.filter_by(is_active=True)
        elif is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        
        if is_featured is not None:
            query = query.filter_by(is_featured=is_featured.lower() == 'true')
        
        query = query.order_by(Testimonial.order_position, Testimonial.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        testimonials = query.all()
        
        return jsonify({
            'testimonials': [testimonial.to_dict() for testimonial in testimonials],
            'total': len(testimonials)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<testimonial_id>', methods=['GET'])
def get_testimonial(testimonial_id):
    """Get single testimonial by ID"""
    try:
        testimonial = Testimonial.query.get(testimonial_id)
        
        if not testimonial:
            return jsonify({'error': 'Testimonial not found'}), 404
        
        return jsonify({'testimonial': testimonial.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_testimonial():
    """Create new testimonial (Admin only)"""
    try:
        data = request.get_json()
        
        testimonial = Testimonial(
            client_name=data.get('client_name'),
            client_position=data.get('client_position'),
            client_company=data.get('client_company'),
            client_avatar=data.get('client_avatar'),
            testimonial_text=data.get('testimonial_text'),
            rating=data.get('rating', 5),
            project_type=data.get('project_type'),
            metrics=data.get('metrics', {}),
            is_featured=data.get('is_featured', False),
            order_position=data.get('order_position', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(testimonial)
        db.session.commit()
        
        return jsonify({
            'message': 'Testimonial created successfully',
            'testimonial': testimonial.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<testimonial_id>', methods=['PUT'])
@jwt_required()
def update_testimonial(testimonial_id):
    """Update testimonial (Admin only)"""
    try:
        testimonial = Testimonial.query.get(testimonial_id)
        
        if not testimonial:
            return jsonify({'error': 'Testimonial not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'client_name' in data:
            testimonial.client_name = data['client_name']
        if 'client_position' in data:
            testimonial.client_position = data['client_position']
        if 'client_company' in data:
            testimonial.client_company = data['client_company']
        if 'client_avatar' in data:
            testimonial.client_avatar = data['client_avatar']
        if 'testimonial_text' in data:
            testimonial.testimonial_text = data['testimonial_text']
        if 'rating' in data:
            testimonial.rating = data['rating']
        if 'project_type' in data:
            testimonial.project_type = data['project_type']
        if 'metrics' in data:
            testimonial.metrics = data['metrics']
        if 'is_featured' in data:
            testimonial.is_featured = data['is_featured']
        if 'order_position' in data:
            testimonial.order_position = data['order_position']
        if 'is_active' in data:
            testimonial.is_active = data['is_active']
        
        testimonial.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Testimonial updated successfully',
            'testimonial': testimonial.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<testimonial_id>', methods=['DELETE'])
@jwt_required()
def delete_testimonial(testimonial_id):
    """Delete testimonial (Admin only)"""
    try:
        testimonial = Testimonial.query.get(testimonial_id)
        
        if not testimonial:
            return jsonify({'error': 'Testimonial not found'}), 404
        
        db.session.delete(testimonial)
        db.session.commit()
        
        return jsonify({'message': 'Testimonial deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
