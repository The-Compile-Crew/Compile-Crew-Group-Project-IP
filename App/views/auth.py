from flask import Blueprint, render_template, request, flash, send_from_directory, flash, redirect, url_for, session


from.index import index_views

from App.controllers import (
    login,
    create_user,
)
from App.controllers.controllers.simple_auth import simple_login, simple_signup
from App.controllers import (
    get_shortlist_by_student,
    get_positions_by_employer
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''
# Simple login/signup routes (for the login.html form)
@auth_views.route('/simple_login', methods=['POST'])
def simple_login_route():
    return simple_login()

@auth_views.route('/simple_signup', methods=['POST'])
def simple_signup_route():
    return simple_signup()

@auth_views.route('/student-dashboard')
def student_dashboard():
    username = session.get('username')
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    applications = []
    try:
        applications = get_shortlist_by_student(user_id) or []
    except Exception:
        applications = []
    return render_template('StudentDashboard.html', username=username, applications=applications)

@auth_views.route('/employerdashboard')
def employer_dashboard():
    username = session.get('username')
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    positions = []
    try:
        positions = get_positions_by_employer(user_id) or []
    except Exception:
        positions = []
    return render_template('EmployerDashboard.html', username=username, positions=positions)

@auth_views.route('/StaffDashboard')
def staff_dashboard():
    username = session.get('username')
    from App.models.student import Student
    from App.models.position import Position
    students = Student.query.all()
    positions = Position.query.all()
    return render_template('StaffDashboard.html', username=username, students=students, positions=positions)


@auth_views.route('/login', methods=['POST'])
def login_action():
    # Legacy JWT login removed for UI-only mode. Redirect back.
    flash('Use the login form on the home page.' )
    return redirect(request.referrer or '/')

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    # Legacy JWT signup removed for UI-only mode. Use the simple signup form.
    flash('Use the signup form on the home page.')
    return redirect(request.referrer or '/')


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    # Clear server-side session and redirect to login page
    session.clear()
    flash('Logged out')
    return redirect('/')

'''
API Routes
'''

# JSON API routes removed for UI-only project requirements.