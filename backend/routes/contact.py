from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models import ContactMessage
from datetime import datetime

bp = Blueprint('contact', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_contact_messages():
    """Get all contact messages (Admin only)"""
    try:
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        
        query = ContactMessage.query
        
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(ContactMessage.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        messages = query.all()
        
        return jsonify({
            'messages': [message.to_dict() for message in messages],
            'total': len(messages)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<message_id>', methods=['GET'])
@jwt_required()
def get_contact_message(message_id):
    """Get single contact message by ID (Admin only)"""
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        # Mark as read
        if message.status == 'new':
            message.status = 'read'
            message.updated_at = datetime.utcnow()
            db.session.commit()
        
        return jsonify({'message': message.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/submit', methods=['POST'])
def submit_contact_form():
    """Submit contact form (Public)"""
    try:
        data = request.get_json()
        
        name = data.get('name')
        email = data.get('email')
        message_text = data.get('message')
        
        if not name or not email or not message_text:
            return jsonify({'error': 'Name, email and message are required'}), 400
        
        # Create contact message
        message = ContactMessage(
            name=name,
            email=email,
            phone=data.get('phone'),
            subject=data.get('subject'),
            message=message_text,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:300],
            status='new'
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent successfully',
            'id': message.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<message_id>', methods=['PUT'])
@jwt_required()
def update_contact_message_status(message_id):
    """Update contact message status (Admin only)"""
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            message.status = data['status']
        
        message.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Status updated successfully',
            'contact_message': message.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<message_id>', methods=['DELETE'])
@jwt_required()
def delete_contact_message(message_id):
    """Delete contact message (Admin only)"""
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({'message': 'Contact message deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_contact_stats():
    """Get contact messages statistics (Admin only)"""
    try:
        total = ContactMessage.query.count()
        new = ContactMessage.query.filter_by(status='new').count()
        read = ContactMessage.query.filter_by(status='read').count()
        replied = ContactMessage.query.filter_by(status='replied').count()
        archived = ContactMessage.query.filter_by(status='archived').count()
        
        return jsonify({
            'stats': {
                'total': total,
                'new': new,
                'read': read,
                'replied': replied,
                'archived': archived
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
