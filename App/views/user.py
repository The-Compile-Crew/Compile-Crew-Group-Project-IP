from flask import Blueprint, render_template, request, send_from_directory, flash, redirect, url_for, session
from App.controllers import (
    create_user,
    get_all_users
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    # API endpoints removed for UI-only requirement; redirect to server-rendered users page
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    # API endpoints removed; create user via server-rendered form
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')
