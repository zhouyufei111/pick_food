from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50))  # 添加username字段
    phone = db.Column(db.String(20))     # 添加phone字段
    nickname = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255))
    session_key = db.Column(db.String(50))  # 添加session_key字段
    last_login = db.Column(db.DateTime)  # 添加最后登录时间字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username or self.nickname or '',  # 优先使用username，其次是nickname
            'phone': self.phone or '',
            'nickname': self.nickname or '',
            'avatar_url': self.avatar_url or '',
            'openid': self.openid,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    activity_level = db.Column(db.Enum('sedentary', 'light', 'moderate', 'active', 'very_active'))
    bmr = db.Column(db.Numeric(8, 2))
    tdee = db.Column(db.Numeric(8, 2))
    calorie_target = db.Column(db.Numeric(8, 2))
    protein_target = db.Column(db.Numeric(6, 2))
    fat_target = db.Column(db.Numeric(6, 2))
    carb_target = db.Column(db.Numeric(6, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'height': float(self.height) if self.height else None,
            'weight': float(self.weight) if self.weight else None,
            'age': self.age,
            'gender': self.gender,
            'activity_level': self.activity_level,
            'bmr': float(self.bmr) if self.bmr else None,
            'tdee': float(self.tdee) if self.tdee else None,
            'calorie_target': float(self.calorie_target) if self.calorie_target else None,
            'protein_target': float(self.protein_target) if self.protein_target else None,
            'fat_target': float(self.fat_target) if self.fat_target else None,
            'carb_target': float(self.carb_target) if self.carb_target else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 