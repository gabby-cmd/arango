from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-this-in-production')

def create_user(username, email, password, role):
    """Create a new user"""
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        raise ValueError("User with this email already exists")
    if User.query.filter_by(username=username).first():
        raise ValueError("User with this username already exists")
    
    # Create new user
    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    """Authenticate user and return user object if valid"""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def generate_token(user):
    """Generate JWT token for user"""
    payload = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow().timestamp() + (7 * 24 * 60 * 60)  # 7 days
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()

