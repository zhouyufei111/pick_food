from flask import Blueprint, jsonify, request
from models import db
from models.user import User, UserProfile
from middleware.auth import token_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/list', methods=['GET'])
@token_required
def get_users(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(User.username.like(f'%{search}%'))
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })

@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@users_bp.route('/<int:user_id>/profile', methods=['GET'])
@token_required
def get_user_profile(current_user, user_id):
    user = User.query.get_or_404(user_id)
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        return jsonify({'message': '用户资料不存在'}), 404
    
    user_data = user.to_dict()
    user_data['profile'] = profile.to_dict()
    
    return jsonify(user_data)

@users_bp.route('/<int:user_id>/food_records', methods=['GET'])
@token_required
def get_user_food_records(current_user, user_id):
    from models.food_record import FoodRecord
    
    user = User.query.get_or_404(user_id)
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = FoodRecord.query.filter_by(user_id=user_id)
    
    if start_date:
        query = query.filter(FoodRecord.record_date >= start_date)
    if end_date:
        query = query.filter(FoodRecord.record_date <= end_date)
    
    records = query.order_by(FoodRecord.record_date.desc()).all()
    
    return jsonify([record.to_dict() for record in records])

@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data and data['username'] != user.username:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'message': '用户名已存在'}), 409
        user.username = data['username']
    
    if 'password' in data:
        user.set_password(data['password'])
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    try:
        db.session.commit()
        return jsonify({'message': '用户更新成功', 'user': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'更新失败: {str(e)}'}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if current_user.id == user_id:
        return jsonify({'message': '不能删除当前登录的用户'}), 403
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': '用户删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'删除失败: {str(e)}'}), 500 