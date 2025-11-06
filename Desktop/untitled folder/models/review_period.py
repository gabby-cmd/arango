from extensions import db
from datetime import datetime, date

class ReviewPeriod(db.Model):
    __tablename__ = 'review_periods'

    id = db.Column(db.Integer, primary_key=True)
    period_name = db.Column(db.String(100), nullable=False)
    period_type = db.Column(db.String(50), nullable=False)  # 'Q1', 'Q2', 'Q3', 'Q4', 'Annual', etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    financial_period = db.Column(db.String(50))  # e.g., 'FY2024', 'FY2025'
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='Draft')  # 'Draft', 'Open', 'Closed'
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __init__(self, period_name, period_type, start_date, end_date, financial_period, description, created_by, status='Draft'):
        self.period_name = period_name
        self.period_type = period_type
        self.start_date = start_date
        self.end_date = end_date
        self.financial_period = financial_period
        self.description = description
        self.created_by = created_by
        self.status = status

    def open_period(self):
        """Open the review period"""
        self.status = 'Open'
        self.updated_at = datetime.utcnow()

    def close_period(self):
        """Close the review period"""
        self.status = 'Closed'
        self.updated_at = datetime.utcnow()

    def is_open(self):
        """Check if period is currently open"""
        return self.status == 'Open'

    def is_closed(self):
        """Check if period is closed"""
        return self.status == 'Closed'

    def to_dict(self):
        return {
            'id': self.id,
            'period_name': self.period_name,
            'period_type': self.period_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'financial_period': self.financial_period,
            'description': self.description,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

