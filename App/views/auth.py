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
    from App.models.position import Position
    from App.models.shortlist import Shortlist, DecisionStatus
    from App.models.student import Student
    student = Student.query.filter_by(user_id=user_id).first()
    # Get all open positions
    from App.models.position import PositionStatus
    # Always use PositionStatus.open for filtering
    open_positions = Position.query.filter_by(status=PositionStatus.open).all()
    open_position_ids = {pos.id for pos in open_positions}
    # Get all shortlist entries for this student for open positions only
    shortlist_entries = Shortlist.query.filter(Shortlist.student_id==student.id, Shortlist.position_id.in_(open_position_ids)).all() if student else []

    # Build a dict to ensure one application per position (prefer shortlist entry)
    applications_dict = {}
    for entry in shortlist_entries:
        # Ensure status is always an enum
        if isinstance(entry.status, str):
            try:
                entry.status = DecisionStatus(entry.status)
            except Exception:
                pass
        applications_dict[entry.position_id] = entry

    for pos in open_positions:
        if pos.id not in applications_dict:
            # Create a mock application object for 'applied' state
            class MockApp:
                pass
            mock = MockApp()
            mock.position = pos
            mock.status = DecisionStatus.applied
            mock.student_id = student.id if student else None
            applications_dict[pos.id] = mock

    applications = list(applications_dict.values())
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
    user_id = session.get('user_id')
    
    # Require authentication
    if not user_id or not username:
        return redirect('/')
    
    from App.models.student import Student
    from App.models.position import Position
    from App.models.shortlist import Shortlist
    students = Student.query.all()
    positions = Position.query.filter_by(status='open').all()
    
    # Serialize positions to JSON-compatible format
    positions_json = [p.toJSON() for p in positions]
    
    # Get all shortlist entries (applicants)
    applicants = Shortlist.query.all()
    applicants_json = [a.toJSON() for a in applicants]
    
    return render_template('StaffDashboard.html', 
                         username=username, 
                         students=students, 
                         positions=positions_json,
                         applicants=applicants_json)


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
    return render_template('login.html')

'''
API Routes
'''

# JSON API routes removed for UI-only project requirements.