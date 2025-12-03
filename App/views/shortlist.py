# Route to show decision page for a student's application
from flask import Blueprint, request, redirect, url_for, flash, session, render_template
shortlist_views = Blueprint('shortlist_views', __name__)
from App.controllers import (
     add_student_to_shortlist,
     decide_shortlist,
     get_shortlist_by_student,
     get_shortlist_by_position
)

# Route to show decision page for a student's application
@shortlist_views.route('/shortlist/decision/<int:student_id>/<int:position_id>', methods=['GET'])
def view_decision(student_id, position_id):
    from App.models.shortlist import Shortlist
    shortlist = Shortlist.query.filter_by(student_id=student_id, position_id=position_id).first_or_404()
    return render_template('decision.html', shortlist=shortlist)
# Route to review a student application for a position
@shortlist_views.route('/shortlist/review/<int:student_id>/<int:position_id>', methods=['GET'])
def review_application(student_id, position_id):
    from App.models.shortlist import Shortlist
    shortlist = Shortlist.query.filter_by(student_id=student_id, position_id=position_id).first_or_404()
    return render_template('review.html', shortlist=shortlist)
# Route to show addtoshortlist.html for a given position
@shortlist_views.route('/shortlist/add/<int:position_id>', methods=['GET'])
def show_add_to_shortlist(position_id):
    from App.models.position import Position
    from App.models.student import Student
    position = Position.query.get_or_404(position_id)
    students = Student.query.all()
    return render_template('addtoshortlist.html', position=position, students=students)



# UI-only mode: all routes return HTML or redirects (no JSON APIs)

@shortlist_views.route('/shortlist/add', methods=['POST'])
def add_student_shortlist():
    # Form-based action: staff adds a student to shortlist
    staff_user_id = session.get('user_id')
    if not staff_user_id:
        flash('Not authenticated')
        return redirect(url_for('auth_views.staff_dashboard'))

    student_user_id = request.form.get('student_user_id')
    student_name = request.form.get('student_name')
    student_id = request.form.get('student_id')
    details = request.form.get('details')
    position_id = request.form.get('position_id')
    if not student_user_id or not position_id or not student_name or not student_id or not details:
        flash('Missing parameters')
        return redirect(url_for('auth_views.staff_dashboard'))

    result = add_student_to_shortlist(int(student_user_id), int(position_id), int(staff_user_id), student_name, student_id, details)
    if result:
        flash('Student added to shortlist')
    else:
        flash('Failed to add to shortlist')
    return redirect(url_for('auth_views.staff_dashboard'))


@shortlist_views.route('/shortlist/decide', methods=['POST'])
def shortlist_decide():
    # Employer decides on a shortlist entry via form submit
    employer_user_id = session.get('user_id')
    if not employer_user_id:
        flash('Not authenticated')
        return redirect(url_for('auth_views.employer_dashboard'))

    student_user_id = request.form.get('student_user_id')
    position_id = request.form.get('position_id')
    decision = request.form.get('decision')
    if not student_user_id or not position_id or not decision:
        flash('Missing parameters')
        return redirect(url_for('auth_views.employer_dashboard'))

    result = decide_shortlist(int(student_user_id), int(position_id), decision)
    if result:
        flash('Shortlist updated')
    else:
        flash('Failed to update shortlist')
    return redirect(url_for('auth_views.employer_dashboard'))


@shortlist_views.route('/shortlist/student/<int:student_id>', methods=['GET'])
def view_student_shortlist(student_id):
    # Redirect to student dashboard (shortlist data displayed there server-side)
    return redirect(url_for('auth_views.student_dashboard'))


@shortlist_views.route('/shortlist/position/<int:position_id>', methods=['GET'])
def view_position_shortlist(position_id):
    # Redirect to employer dashboard (shortlist data displayed there server-side)
    return redirect(url_for('auth_views.employer_dashboard'))
