from extensions import db
from datetime import datetime

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True)
    evaluation_type = db.Column(db.String(20), nullable=False)
    performance_document_id = db.Column(db.Integer, db.ForeignKey('performance_documents.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ratings = db.Column(db.JSON, nullable=False)
    comments = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='Draft')
    submitted_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    performance_document = db.relationship('PerformanceDocument', foreign_keys=[performance_document_id])
    employee = db.relationship('User', foreign_keys=[employee_id])
    evaluator = db.relationship('User', foreign_keys=[evaluator_id])

    @property
    def summary(self):
        return {
            'type': self.evaluation_type,
            'status': self.status,
            'submitted': self.submitted_at.isoformat() if self.submitted_at else 'Not submitted',
            'approved': self.approved_at.isoformat() if self.approved_at else 'Not approved'
        }

    def to_dict(self):
        return {
            'id': self.id,
            'evaluation_type': self.evaluation_type,
            'performance_document_id': self.performance_document_id,
            'employee_id': self.employee_id,
            'evaluator_id': self.evaluator_id,
            'ratings': self.ratings,
            'comments': self.comments,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }