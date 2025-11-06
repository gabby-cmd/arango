from extensions import db
from datetime import datetime

class PerformanceDocument(db.Model):
    __tablename__ = 'performance_documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Draft')
    version = db.Column(db.Integer, default=1)
    published_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id])
    goals = db.relationship('Goal', backref='performance_document', lazy=True)
    competencies = db.relationship('Competency', backref='performance_document', lazy=True)
    evaluations = db.relationship('Evaluation', backref='document', lazy=True)

    # Approval history as a JSON column
    approval_history = db.Column(db.JSON, default=[])

    @property
    def current_approval_status(self):
        if self.approval_history:
            return self.approval_history[-1]['status']
        return 'Not Started'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'owner_id': self.owner_id,
            'status': self.status,
            'version': self.version,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'approval_status': self.current_approval_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }