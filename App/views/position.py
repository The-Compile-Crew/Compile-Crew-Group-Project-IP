from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from App.controllers import (
    open_position,
    get_positions_by_employer
)
from App.database import db

position_views = Blueprint('position_views', __name__, template_folder='../templates')

# API endpoints removed for UI-only requirement; use server-rendered /positions views instead
@position_views.route('/api/positions/all', methods=['GET'])
def get_all_positions_api():
    return redirect(url_for('position_views.list_positions_page'))

@position_views.route('/api/positions/create', methods=['POST'])
def create_position_api():
    return redirect(url_for('position_views.list_positions_page'))

@position_views.route('/api/employer/positions', methods=['GET'])
def get_employer_positions_api():
    return redirect(url_for('position_views.list_positions_page'))

# List all positions (UI) with search/filter
@position_views.route('/positions', methods=['GET'])
def list_positions_page():
    from App.models.position import Position

    search = request.args.get('search', '')
    status = request.args.get('status', '')

    query = Position.query

    if search:
        query = query.filter(Position.title.ilike(f"%{search}%"))
    if status:
        query = query.filter(Position.status == status)

    positions = query.all()
    return render_template('positions/list.html', positions=positions)

# Create position form (UI)
@position_views.route('/positions/create', methods=['GET', 'POST'])
def create_position_page():
    # session-based employer check
    if session.get('user_type') != 'employer':
        flash("Unauthorized user", "error")
        return redirect('/')

    if request.method == 'POST':
        title = request.form.get('title')
        capacity = request.form.get('capacity')
        
        if not title or not capacity:
            flash("Missing required fields", "error")
            return redirect(url_for('position_views.create_position_page'))
        
        user_id = session.get('user_id')

        pos = open_position(user_id, title, int(capacity))
        if pos:
            db.session.commit()
            flash("Position created successfully!", "success")
            return redirect(url_for('auth_views.employer_dashboard'))
        else:
            flash("Failed to create position", "error")
            return redirect(url_for('position_views.create_position_page'))

    return render_template('positions/create.html', position=None)

# Position detail view (UI)
@position_views.route('/positions/<int:id>', methods=['GET'])
def position_detail_page(id):
    from App.models.position import Position
    pos = Position.query.get_or_404(id)
    return render_template('positions/detail.html', position=pos)

# Edit position form (UI)
@position_views.route('/positions/<int:id>/edit', methods=['GET', 'POST'])
def edit_position_page(id):
    from App.models.position import Position
    pos = Position.query.get_or_404(id)

    # session-based access check
    if session.get('user_type') != 'employer':
        flash("Unauthorized user", "error")
        return redirect(url_for('auth_views.employer_dashboard'))

    if request.method == 'POST':
        pos.title = request.form.get('title', pos.title)
        pos.number_of_positions = int(request.form.get('capacity', pos.number_of_positions))
        db.session.commit()
        flash("Position updated successfully!", "success")
        return redirect(url_for('auth_views.employer_dashboard'))

    return render_template('positions/create.html', position=pos)