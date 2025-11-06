from flask import Flask, jsonify, request
from extensions import db, migrate
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)

# Import models after db initialization
from models.user import User
from models.goal import Goal
from models.competency import Competency
from models.performance_document import PerformanceDocument
from models.evaluation import Evaluation
from models.notification import Notification
from models.review_period import ReviewPeriod
from services.auth_service import create_user, authenticate_user, generate_token
from services.goal_service import create_goal, get_user_goals
from services.competency_service import create_competency, get_user_competencies
from services.performance_document_service import create_performance_document, get_user_documents
from services.evaluation_service import create_evaluation, get_user_evaluations
from services.notification_service import create_notification, get_unread_notifications, mark_notification_as_read
from services.review_period_service import (
    create_review_period, get_all_review_periods, get_review_period_by_id,
    update_review_period, delete_review_period, open_review_period, close_review_period
)
from middleware.auth import authenticate_token, authorize_role

# Auth Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = create_user(data['username'], data['email'], data['password'], data['role'])
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = generate_token(user)
    return jsonify({'token': token, 'user': user.to_dict()})

# Goal Routes
@app.route('/api/goals', methods=['POST'])
@authenticate_token
def create_goal_route():
    data = request.get_json()
    goal = create_goal(data['user_id'], data['title'], data['description'], data['start_date'], data['end_date'])
    return jsonify(goal.to_dict()), 201

@app.route('/api/users/<user_id>/goals', methods=['GET'])
@authenticate_token
def get_user_goals_route(user_id):
    goals = get_user_goals(user_id)
    return jsonify([goal.to_dict() for goal in goals])

# Competency Routes
@app.route('/api/competencies', methods=['POST'])
@authenticate_token
@authorize_role(['HR', 'Manager'])
def create_competency_route():
    data = request.get_json()
    competency = create_competency(data['title'], data['description'], data['level'])
    return jsonify(competency.to_dict()), 201

@app.route('/api/users/<user_id>/competencies', methods=['GET'])
@authenticate_token
def get_user_competencies_route(user_id):
    competencies = get_user_competencies(user_id)
    return jsonify([competency.to_dict() for competency in competencies])

# Performance Document Routes
@app.route('/api/performance-documents', methods=['POST'])
@authenticate_token
@authorize_role(['Manager', 'HR'])
def create_performance_document_route():
    data = request.get_json()
    document = create_performance_document(
        data['user_id'], 
        data['title'], 
        data['period_start'], 
        data['period_end'], 
        data['status']
    )
    return jsonify(document.to_dict()), 201

@app.route('/api/users/<user_id>/performance-documents', methods=['GET'])
@authenticate_token
def get_user_documents_route(user_id):
    documents = get_user_documents(user_id)
    return jsonify([doc.to_dict() for doc in documents])

# Evaluation Routes
@app.route('/api/evaluations', methods=['POST'])
@authenticate_token
def create_evaluation_route():
    data = request.get_json()
    evaluation = create_evaluation(
        data['document_id'], 
        data['evaluator_id'], 
        data['type'], 
        data['comments'], 
        data['rating']
    )
    return jsonify(evaluation.to_dict()), 201

@app.route('/api/users/<user_id>/evaluations', methods=['GET'])
@authenticate_token
def get_user_evaluations_route(user_id):
    evaluations = get_user_evaluations(user_id)
    return jsonify([eval.to_dict() for eval in evaluations])

# Notification Routes
@app.route('/api/notifications', methods=['POST'])
@authenticate_token
@authorize_role(['HR', 'Manager'])
def create_notification_route():
    data = request.get_json()
    notification = create_notification(
        data['recipient_id'], 
        data['message'], 
        data['entity_type'], 
        data['entity_id']
    )
    return jsonify(notification.to_dict()), 201

@app.route('/api/notifications/unread', methods=['GET'])
@authenticate_token
def get_unread_notifications_route():
    notifications = get_unread_notifications(request.user['id'])
    return jsonify([n.to_dict() for n in notifications])

@app.route('/api/notifications/<notification_id>/read', methods=['PATCH'])
@authenticate_token
def mark_notification_as_read_route(notification_id):
    notification = mark_notification_as_read(notification_id)
    return jsonify(notification.to_dict())

# Review Period Routes
@app.route('/api/review-periods', methods=['GET'])
@authenticate_token
def get_all_review_periods_route():
    """Get all review periods"""
    periods = get_all_review_periods()
    return jsonify([period.to_dict() for period in periods])

@app.route('/api/review-periods', methods=['POST'])
@authenticate_token
@authorize_role(['HR', 'Admin'])
def create_review_period_route():
    """Create a new review period (HR only)"""
    data = request.get_json()
    try:
        from datetime import datetime
        period = create_review_period(
            period_name=data['period_name'],
            period_type=data['period_type'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            financial_period=data.get('financial_period'),
            description=data.get('description'),
            created_by=request.user['id']
        )
        return jsonify(period.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/review-periods/<period_id>', methods=['GET'])
@authenticate_token
def get_review_period_route(period_id):
    """Get review period by ID"""
    period = get_review_period_by_id(period_id)
    if not period:
        return jsonify({'error': 'Review period not found'}), 404
    return jsonify(period.to_dict())

@app.route('/api/review-periods/<period_id>', methods=['PUT'])
@authenticate_token
@authorize_role(['HR', 'Admin'])
def update_review_period_route(period_id):
    """Update review period (HR only)"""
    data = request.get_json()
    try:
        from datetime import datetime
        update_data = {}
        if 'period_name' in data:
            update_data['period_name'] = data['period_name']
        if 'period_type' in data:
            update_data['period_type'] = data['period_type']
        if 'start_date' in data:
            update_data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            update_data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        if 'financial_period' in data:
            update_data['financial_period'] = data['financial_period']
        if 'description' in data:
            update_data['description'] = data['description']
        
        period = update_review_period(period_id, **update_data)
        if not period:
            return jsonify({'error': 'Review period not found'}), 404
        return jsonify(period.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/review-periods/<period_id>', methods=['DELETE'])
@authenticate_token
@authorize_role(['HR', 'Admin'])
def delete_review_period_route(period_id):
    """Delete review period (HR only)"""
    if delete_review_period(period_id):
        return jsonify({'message': 'Review period deleted successfully'}), 200
    return jsonify({'error': 'Review period not found'}), 404

@app.route('/api/review-periods/<period_id>/open', methods=['POST'])
@authenticate_token
@authorize_role(['HR', 'Admin'])
def open_review_period_route(period_id):
    """Open a review period (HR only)"""
    period = open_review_period(period_id)
    if not period:
        return jsonify({'error': 'Review period not found'}), 404
    return jsonify(period.to_dict())

@app.route('/api/review-periods/<period_id>/close', methods=['POST'])
@authenticate_token
@authorize_role(['HR', 'Admin'])
def close_review_period_route(period_id):
    """Close a review period (HR only)"""
    period = close_review_period(period_id)
    if not period:
        return jsonify({'error': 'Review period not found'}), 404
    return jsonify(period.to_dict())

if __name__ == '__main__':
    app.run(debug=True)