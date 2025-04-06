from . import db
from datetime import datetime

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Numeric(8, 2), nullable=False)
    protein = db.Column(db.Numeric(6, 2), nullable=False)
    fat = db.Column(db.Numeric(6, 2), nullable=False)
    carbs = db.Column(db.Numeric(6, 2), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联餐厅
    restaurant = db.relationship('Restaurant', backref=db.backref('food_items', lazy='dynamic'))
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'calories': float(self.calories),
            'protein': float(self.protein),
            'fat': float(self.fat),
            'carbs': float(self.carbs),
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'restaurant_name': self.restaurant.name if self.restaurant else None
        } 