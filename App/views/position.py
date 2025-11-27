from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (
    open_position,
    get_positions_by_employer,
    get_all_positions_json,
    get_positions_by_employer_json
)
from App.database import db

position_views = Blueprint('position_views', __name__, template_folder='../templates')

# Get all positions (API)
@position_views.route('/api/positions/all', methods=['GET'])
def get_all_positions_api():
    position_list = get_all_positions_json()
    return jsonify(position_list), 200

# Create a position (API)
@position_views.route('/api/positions/create', methods=['POST'])
@jwt_required()
def create_position_api():
    if current_user.role != 'employer':
        return jsonify({"message": "Unauthorized user"}), 403
    
    data = request.json
    position = open_position(title=data['title'], user_id=current_user.id, number_of_positions=data['number'])
    
    if position:
        return jsonify(position.toJSON()), 201
    else:
        return jsonify({"error": "Failed to create position"}), 400

# Get positions for a given employer (API)
@position_views.route('/api/employer/positions', methods=['GET'])
@jwt_required()
def get_employer_positions_api():
    if current_user.role != 'employer':
        return jsonify({"message": "Unauthorized user"}), 403
    
    return jsonify(get_positions_by_employer_json(current_user.id)), 200

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
@jwt_required()
def create_position_page():
    if current_user.role != 'employer':
        flash("Unauthorized user")
        return redirect(url_for('position_views.list_positions_page'))

    if request.method == 'POST':
        title = request.form['title']
        number = int(request.form['number'])
        employer_id = current_user.id

        pos = open_position(title, employer_id, number)
        if pos:
            db.session.add(pos)
            db.session.commit()
            flash("Position created successfully!")
            return redirect(url_for('position_views.list_positions_page'))
        else:
            flash("Failed to create position")
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
@jwt_required()
def edit_position_page(id):
    from App.models.position import Position
    pos = Position.query.get_or_404(id)

    if current_user.role != 'employer' or pos.employer_id != current_user.id:
        flash("Unauthorized user")
        return redirect(url_for('position_views.list_positions_page'))

    if request.method == 'POST':
        pos.title = request.form['title']
        pos.number_of_positions = int(request.form['number'])
        db.session.commit()
        flash("Position updated successfully!")
        return redirect(url_for('position_views.position_detail_page', id=pos.id))

    return render_template('positions/create.html', position=pos)