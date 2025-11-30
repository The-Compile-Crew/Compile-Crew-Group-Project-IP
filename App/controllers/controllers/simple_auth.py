from flask import request, jsonify, redirect
from App.controllers.user import create_user
from App.models import User
from App.database import db

def simple_login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('userType')
        
        print(f"Login attempt: username={username}, user_type={user_type}")
        
        # Check if user exists and password is correct
        user = User.query.filter_by(username=username).first()
        print(f"User found: {user}")
        
        if user:
            print(f"User role: {user.role}, checking password...")
            if user.check_password(password) and user.role == user_type:
                # Redirect based on user type
                if user_type == 'student':
                    return redirect('/student-dashboard')
                elif user_type == 'employer':
                    return redirect('/employerdashboard')
                elif user_type == 'staff':
                    return redirect('/StaffDashboard')
        
        # If login fails
        print("Login failed - credentials don't match")
        return "Login failed - check your credentials", 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Server error: {str(e)}", 500

def simple_signup():
    username = request.form.get('username')
    password = request.form.get('password')
    user_type = request.form.get('userType')
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return "Username already exists", 400
    
    # Create new user
    result = create_user(username, password, user_type)
    
    if result:
        return "Account created! You can now login.", 201
    else:
        return "Account creation failed", 400
