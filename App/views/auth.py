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
    from App.models.position import PositionStatus
    open_positions = Position.query.filter_by(status=PositionStatus.open).all()
    open_position_ids = {pos.id for pos in open_positions}
    shortlist_entries = Shortlist.query.filter(Shortlist.student_id==student.id, Shortlist.position_id.in_(open_position_ids)).all() if student else []
    applications_dict = {}
    for entry in shortlist_entries:
        if isinstance(entry.status, str):
            try:
                entry.status = DecisionStatus(entry.status)
            except Exception:
                pass
        entry.position = Position.query.get(entry.position_id)
        applications_dict[entry.position_id] = entry
    for pos in open_positions:
        if pos.id not in applications_dict:
            class MockApp:
                pass
            mock = MockApp()
            mock.position = pos
            mock.status = DecisionStatus.applied
            mock.student_id = student.id if student else None
            applications_dict[pos.id] = mock
    # DEMO: If no applications, add demo data
    if not applications_dict:
        class DemoApp:
            pass
        demo1 = DemoApp()
        demo1.position = type('DemoPosition', (), {'title': 'Software Engineer Intern', 'description': 'Work on real projects.'})
        demo1.status = DecisionStatus.shortlisted
        demo1.student_id = 1
        demo2 = DemoApp()
        demo2.position = type('DemoPosition', (), {'title': 'Marketing Assistant', 'description': 'Assist with campaigns.'})
        demo2.status = DecisionStatus.shortlisted
        demo2.student_id = 2
        applications = [demo1, demo2]
    else:
        applications = list(applications_dict.values())
    return render_template('StudentDashboard.html', username=username, applications=applications)

@auth_views.route('/employerdashboard')
def employer_dashboard():
    username = session.get('username')
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    positions = []
    applicants = []
    try:
        positions = get_positions_by_employer(user_id) or []
        from App.models.shortlist import Shortlist
        from App.models.student import Student
        # DEMO: If no positions, add demo data
        if not positions:
            positions = [
                type('DemoPosition', (), {'id': 1, 'title': 'Software Engineer Intern', 'description': 'Work on real projects.', 'number_of_positions': 2}),
                type('DemoPosition', (), {'id': 2, 'title': 'Marketing Assistant', 'description': 'Assist with campaigns.', 'number_of_positions': 1}),
            ]
        for pos in positions:
            shortlists = Shortlist.query.filter_by(position_id=getattr(pos, 'id', 0)).all() if hasattr(pos, 'id') else []
            # DEMO: If no shortlist, add demo applicants
            if not shortlists:
                if pos.id == 1:
                    applicants.append({'name': 'demo_student1', 'status': 'shortlisted', 'position_name': pos.title})
                if pos.id == 2:
                    applicants.append({'name': 'demo_student2', 'status': 'shortlisted', 'position_name': pos.title})
            for s in shortlists:
                student = Student.query.get(s.student_id)
                applicants.append({
                    'name': student.username if student else 'Unknown',
                    'status': s.status.value if hasattr(s.status, 'value') else s.status,
                    'position_name': pos.title if hasattr(pos, 'title') else pos.name,
                })
    except Exception:
        positions = [
            type('DemoPosition', (), {'id': 1, 'title': 'Software Engineer Intern', 'description': 'Work on real projects.', 'number_of_positions': 2}),
            type('DemoPosition', (), {'id': 2, 'title': 'Marketing Assistant', 'description': 'Assist with campaigns.', 'number_of_positions': 1}),
        ]
        applicants = [
            {'name': 'demo_student1', 'status': 'shortlisted', 'position_name': 'Software Engineer Intern'},
            {'name': 'demo_student2', 'status': 'shortlisted', 'position_name': 'Marketing Assistant'},
        ]
    return render_template('EmployerDashboard.html', username=username, positions=positions, applicants=applicants)

@auth_views.route('/StaffDashboard')
def staff_dashboard():
    username = session.get('username')
    from App.models.position import Position
    from App.models import Student
    students = Student.query.all()
    positions = Position.query.filter_by(status='open').all()
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
    return render_template('login.html')

'''
API Routes
'''

# JSON API routes removed for UI-only project requirements.