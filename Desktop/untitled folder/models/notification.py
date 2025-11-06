from extensions import db
from datetime import datetime
import uuid

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)  # 'Goal', 'PerformanceDocument', 'Evaluation'
    entity_id = db.Column(db.Integer, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recipient = db.relationship('User', foreign_keys=[recipient_id])

    def to_dict(self):
        return {
            'id': self.id,
            'recipient': self.recipient_id,
            'message': self.message,
            'entityType': self.entity_type,
            'entityId': self.entity_id,
            'isRead': self.is_read,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }