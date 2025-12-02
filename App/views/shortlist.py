from flask import Blueprint, request, redirect, url_for, flash, session
from App.controllers import (
    add_student_to_shortlist,
    decide_shortlist,
    get_shortlist_by_student,
    get_shortlist_by_position
)

shortlist_views = Blueprint('shortlist_views', __name__)

# UI-only mode: all routes return HTML or redirects (no JSON APIs)

@shortlist_views.route('/shortlist/add', methods=['POST'])
def add_student_shortlist():
    # Form-based action: staff adds a student to shortlist
    staff_user_id = session.get('user_id')
    if not staff_user_id:
        flash('Not authenticated')
        return redirect(url_for('auth_views.staff_dashboard'))

    student_user_id = request.form.get('student_user_id')
    position_id = request.form.get('position_id')
    if not student_user_id or not position_id:
        flash('Missing parameters')
        return redirect(url_for('auth_views.staff_dashboard'))

    result = add_student_to_shortlist(int(student_user_id), int(position_id), int(staff_user_id))
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
