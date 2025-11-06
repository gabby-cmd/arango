from models.review_period import ReviewPeriod
from extensions import db
from datetime import datetime, date

def create_review_period(period_name, period_type, start_date, end_date, financial_period, description, created_by):
    """Create a new review period"""
    review_period = ReviewPeriod(
        period_name=period_name,
        period_type=period_type,
        start_date=start_date,
        end_date=end_date,
        financial_period=financial_period,
        description=description,
        created_by=created_by,
        status='Draft'
    )
    db.session.add(review_period)
    db.session.commit()
    return review_period

def get_all_review_periods():
    """Get all review periods"""
    return ReviewPeriod.query.order_by(ReviewPeriod.start_date.desc()).all()

def get_review_period_by_id(period_id):
    """Get review period by ID"""
    return ReviewPeriod.query.get(period_id)

def update_review_period(period_id, period_name=None, period_type=None, start_date=None, end_date=None, 
                        financial_period=None, description=None):
    """Update review period"""
    review_period = ReviewPeriod.query.get(period_id)
    if not review_period:
        return None
    
    if period_name:
        review_period.period_name = period_name
    if period_type:
        review_period.period_type = period_type
    if start_date:
        review_period.start_date = start_date
    if end_date:
        review_period.end_date = end_date
    if financial_period:
        review_period.financial_period = financial_period
    if description:
        review_period.description = description
    
    review_period.updated_at = datetime.utcnow()
    db.session.commit()
    return review_period

def delete_review_period(period_id):
    """Delete review period"""
    review_period = ReviewPeriod.query.get(period_id)
    if review_period:
        db.session.delete(review_period)
        db.session.commit()
        return True
    return False

def open_review_period(period_id):
    """Open a review period"""
    review_period = ReviewPeriod.query.get(period_id)
    if review_period:
        review_period.open_period()
        db.session.commit()
        return review_period
    return None

def close_review_period(period_id):
    """Close a review period"""
    review_period = ReviewPeriod.query.get(period_id)
    if review_period:
        review_period.close_period()
        db.session.commit()
        return review_period
    return None

