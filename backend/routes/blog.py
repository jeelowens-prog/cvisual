from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models import BlogPost
from datetime import datetime
import re

bp = Blueprint('blog', __name__)

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

@bp.route('/', methods=['GET'])
def get_blog_posts():
    """Get all blog posts (public - only published)"""
    try:
        status = request.args.get('status', 'published')
        category = request.args.get('category')
        limit = request.args.get('limit', type=int)
        
        query = BlogPost.query
        
        # Public access only shows published posts
        if not request.headers.get('Authorization'):
            query = query.filter_by(status='published')
        elif status:
            query = query.filter_by(status=status)
        
        if category:
            query = query.filter_by(category=category)
        
        query = query.order_by(BlogPost.published_at.desc(), BlogPost.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        posts = query.all()
        
        return jsonify({
            'posts': [post.to_dict() for post in posts],
            'total': len(posts)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<slug>', methods=['GET'])
def get_blog_post(slug):
    """Get single blog post by slug"""
    try:
        post = BlogPost.query.filter_by(slug=slug).first()
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        # Only show published posts to public
        if post.status != 'published' and not request.headers.get('Authorization'):
            return jsonify({'error': 'Blog post not found'}), 404
        
        # Increment views
        post.views_count += 1
        db.session.commit()
        
        return jsonify({'post': post.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_blog_post():
    """Create new blog post (Admin only)"""
    try:
        data = request.get_json()
        
        title = data.get('title')
        slug = data.get('slug') or slugify(title)
        
        # Check if slug already exists
        if BlogPost.query.filter_by(slug=slug).first():
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
        
        post = BlogPost(
            title=title,
            slug=slug,
            excerpt=data.get('excerpt'),
            content=data.get('content'),
            featured_image=data.get('featured_image'),
            author=data.get('author', 'CVisual Team'),
            category=data.get('category'),
            tags=data.get('tags', []),
            status=data.get('status', 'draft')
        )
        
        if data.get('status') == 'published' and not post.published_at:
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Blog post created successfully',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<post_id>', methods=['PUT'])
@jwt_required()
def update_blog_post(post_id):
    """Update blog post (Admin only)"""
    try:
        post = BlogPost.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            post.title = data['title']
        if 'slug' in data:
            post.slug = data['slug']
        if 'excerpt' in data:
            post.excerpt = data['excerpt']
        if 'content' in data:
            post.content = data['content']
        if 'featured_image' in data:
            post.featured_image = data['featured_image']
        if 'author' in data:
            post.author = data['author']
        if 'category' in data:
            post.category = data['category']
        if 'tags' in data:
            post.tags = data['tags']
        if 'status' in data:
            post.status = data['status']
            if data['status'] == 'published' and not post.published_at:
                post.published_at = datetime.utcnow()
        
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Blog post updated successfully',
            'post': post.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_blog_post(post_id):
    """Delete blog post (Admin only)"""
    try:
        post = BlogPost.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Blog post not found'}), 404
        
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({'message': 'Blog post deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
