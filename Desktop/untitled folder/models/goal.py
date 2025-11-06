from extensions import db
from datetime import datetime

class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    metrics = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id])

    def __init__(self, title, description, owner_id, start_date, end_date):
        self.title = title
        self.description = description
        self.owner_id = owner_id
        self.start_date = start_date
        self.end_date = end_date

    @property
    def duration(self):
        return (self.end_date - self.start_date).days

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner_id': self.owner_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'metrics': self.metrics,
            'duration': self.duration,
            'created_at': self.created_at.isoformat()
        }