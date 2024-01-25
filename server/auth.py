from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)

# Signup
@auth.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json

        # Check if the username or email is already taken
        existing_user = User.query.filter_by(username=data['username']).first()
        existing_email = User.query.filter_by(email=data['email']).first()

        if existing_user or existing_email:
            return jsonify({'message': 'Username or email already exists'}), 400

        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            age=data['age'],
            height=data['height'],
            blood_type=data['blood_type'],
            previous_illnesses=data['previous_illnesses']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Login 
@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            login_user(user)

            # Create a dictionary with user data to include in the response
            user_data = {
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'age': user.age,
                'height': user.height,
                'blood_type': user.blood_type,
                'previous_illnesses': user.previous_illnesses
                # Add more fields as needed
            }

            return jsonify({'message': 'Login successful', 'user_data': user_data}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Logout
@auth.route('/logout', methods=['POST'])
def logout():
    try:
        if current_user.is_authenticated:
            logout_user()
            return jsonify({'message': 'Logout successful'}), 200
        else:
            return jsonify({'message': 'Not logged in'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
