from flask import request, jsonify, redirect, session
from App.controllers.user import create_user
from App.models import User
from App.database import db

def simple_login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        print(f"Login attempt: username={username}, user_type={user_type}")
        
        # Check if user exists and password is correct
        user = User.query.filter_by(username=username).first()
        print(f"User found: {user}")
        
        if user:
            print(f"User role: {user.role}, checking password...")
            if user.check_password(password) and user.role == user_type:
                # store user info in the session so frontend can fetch it
                try:
                    session['user_id'] = user.id
                    session['username'] = user.username
                    session['user_type'] = user.role
                except Exception:
                    # if session can't be set for some reason, continue without failing
                    pass
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
    user_type = request.form.get('user_type')
    student_id = request.form.get('student_id')
    print(f"Signup received: username={username}, user_type={user_type}, student_id={student_id}")

    # Input validation
    if not username or not password or not user_type:
        return "Missing required fields", 400

    if user_type == 'student' and not student_id:
        return "Student ID required for student accounts", 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return "Username already exists", 400

    # Create new user
    if user_type == 'student':
        result = create_user(username, password, user_type, student_id)
        print(f"Student created with student_id={student_id}")
    else:
        result = create_user(username, password, user_type)

    from flask import flash, redirect
    if result:
        flash("Account created! You can now login.", "success")
        return redirect('/')
    else:
        flash("Account creation failed", "error")
        return redirect('/')
