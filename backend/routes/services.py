from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Service
from datetime import datetime

bp = Blueprint('services', __name__)

@bp.route('/', methods=['GET'])
def get_services():
    """Get all services (public)"""
    try:
        is_active = request.args.get('is_active')
        
        query = Service.query
        
        # Public access only shows active services
        if not request.headers.get('Authorization'):
            query = query.filter_by(is_active=True)
        elif is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        
        services = query.order_by(Service.order_position, Service.created_at).all()
        
        return jsonify({
            'services': [service.to_dict() for service in services],
            'total': len(services)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<service_id>', methods=['GET'])
def get_service(service_id):
    """Get single service by ID"""
    try:
        service = Service.query.get(service_id)
        
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        
        return jsonify({'service': service.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    """Create new service (Admin only)"""
    try:
        data = request.get_json()
        
        service = Service(
            title=data.get('title'),
            description=data.get('description'),
            icon=data.get('icon'),
            image_url=data.get('image_url'),
            features=data.get('features', []),
            pricing=data.get('pricing'),
            order_position=data.get('order_position', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'message': 'Service created successfully',
            'service': service.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    """Update service (Admin only)"""
    try:
        service = Service.query.get(service_id)
        
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            service.title = data['title']
        if 'description' in data:
            service.description = data['description']
        if 'icon' in data:
            service.icon = data['icon']
        if 'image_url' in data:
            service.image_url = data['image_url']
        if 'features' in data:
            service.features = data['features']
        if 'pricing' in data:
            service.pricing = data['pricing']
        if 'order_position' in data:
            service.order_position = data['order_position']
        if 'is_active' in data:
            service.is_active = data['is_active']
        
        service.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Service updated successfully',
            'service': service.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    """Delete service (Admin only)"""
    try:
        service = Service.query.get(service_id)
        
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({'message': 'Service deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
