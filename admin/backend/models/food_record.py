from . import db
from datetime import datetime

class FoodRecord(db.Model):
    __tablename__ = 'food_records'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id', ondelete='SET NULL'))
    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack', name='meal_type_enum'), nullable=False)
    custom_food_name = db.Column(db.String(100))
    calories = db.Column(db.Numeric(8, 2), nullable=False)
    protein = db.Column(db.Numeric(6, 2), nullable=False)
    fat = db.Column(db.Numeric(6, 2), nullable=False)
    carbs = db.Column(db.Numeric(6, 2), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    record_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户和食物项
    user = db.relationship('User', backref=db.backref('food_records', lazy='dynamic'))
    food_item = db.relationship('FoodItem', backref=db.backref('records', lazy='dynamic'))
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_item_id': self.food_item_id,
            'meal_type': self.meal_type,
            'custom_food_name': self.custom_food_name,
            'calories': float(self.calories),
            'protein': float(self.protein),
            'fat': float(self.fat),
            'carbs': float(self.carbs),
            'record_date': self.record_date.strftime('%Y-%m-%d'),
            'record_time': self.record_time.strftime('%H:%M:%S'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'food_item': self.food_item.to_dict() if self.food_item else None
        } 