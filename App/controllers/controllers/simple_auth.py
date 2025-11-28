from flask import request, jsonify, redirect
from App.controllers.auth import login
from App.controllers.user import User
from App.database import db

def simple_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_type = request.form.get('userType')
    
    # Check if user exists and password is correct
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password) and user.role == user_type:
        # Redirect based on user type
        if user_type == 'student':
            return redirect('/student-dashboard')
        elif user_type == 'employer':
            return redirect('/employerdashboard')
        elif user_type == 'staff':
            return redirect('/StaffDashboard')
    
    # If login fails
    return "Login failed - check your credentials", 401

def simple_signup():
    username = request.form.get('username')
    password = request.form.get('password')
    user_type = request.form.get('userType')
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return "Username already exists", 400
    
    # Create new user
    new_user = User(username=username, password=password, role=user_type)
    db.session.add(new_user)
    db.session.commit()
    
    return "Account created! You can now login.", 201