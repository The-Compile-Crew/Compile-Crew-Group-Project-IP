import sys
import traceback
from datetime import datetime

def main():
    try:
        print("=" * 50)
        print("Starting Flask Internship Platform")
        print("=" * 50)
        
        # Try to import all modules
        print("\n[1/4] Importing modules...")
        from flask import Flask, render_template, jsonify, request, redirect, url_for, session
        from flask_cors import CORS
        from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
        import os
        from datetime import timedelta
        
        print("✓ All imports successful")
        
        # Initialize Flask app
        print("\n[2/4] Initializing Flask app...")
        app = Flask(__name__)
        
        # Configure app
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-12345')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
        print("✓ App configuration set")
        
        # Enable CORS
        CORS(app, supports_credentials=True)
        print("✓ CORS enabled")
        
        # Initialize JWT
        jwt = JWTManager(app)
        print("✓ JWT initialized")
        
        # Mock user data
        print("\n[3/4] Setting up mock data...")
        users = {
            'johndoe': {
                'id': 1,
                'username': 'johndoe',
                'password': 'password123',
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'type': 'student'
            },
            'janedoe': {
                'id': 2,
                'username': 'janedoe',
                'password': 'password123',
                'name': 'Jane Doe',
                'email': 'jane.doe@example.com',
                'type': 'student'
            },
            'employer1': {
                'id': 3,
                'username': 'employer1',
                'password': 'password123',
                'name': 'Tech Corp HR',
                'email': 'hr@techcorp.com',
                'type': 'employer'
            },
            'employer2': {
                'id': 4,
                'username': 'employer2',
                'password': 'password123',
                'name': 'Data Inc Manager',
                'email': 'manager@datainc.com',
                'type': 'employer'
            }
        }
        
        # Mock applications data for students
        applications = [
            {
                'id': 1,
                'user_id': 1,
                'position_name': "Software Developer Intern",
                'company': "Tech Corp",
                'description': "Develop and maintain web applications using modern frameworks. Work with a team of experienced developers.",
                'status': "pending",
                'applied_date': "2024-03-15",
                'last_updated': "2024-03-20",
                'details': {
                    'feedback': "Your application is currently under review by our hiring team.",
                    'submitted_date': "2024-03-15",
                    'screening_stage': "Initial Screening"
                }
            },
            {
                'id': 2,
                'user_id': 1,
                'position_name': "Data Analyst",
                'company': "Data Inc",
                'description': "Analyze business data and create reports. Work with SQL, Python, and data visualization tools.",
                'status': "accepted",
                'applied_date': "2024-03-10",
                'last_updated': "2024-03-25",
                'details': {
                    'feedback': "Congratulations! Your application has been accepted.",
                    'submitted_date': "2024-03-10",
                    'interview_date': "2024-10-15",
                    'interviewer': "Sarah Johnson",
                    'interview_time': "2:00 PM EST",
                    'location': "Virtual (Zoom)"
                }
            },
            {
                'id': 3,
                'user_id': 1,
                'position_name': "UX Designer",
                'company': "Design Studio",
                'description': "Design user interfaces and experiences for web and mobile applications. Create wireframes and prototypes.",
                'status': "rejected",
                'applied_date': "2024-03-05",
                'last_updated': "2024-03-20",
                'details': {
                    'feedback': "Thank you for your application. Unfortunately, we have decided to move forward with other candidates.",
                    'submitted_date': "2024-03-05"
                }
            },
            {
                'id': 4,
                'user_id': 2,
                'position_name': "Marketing Intern",
                'company': "Marketing Pro",
                'description': "Assist in creating marketing campaigns, social media management, and content creation.",
                'status': "pending",
                'applied_date': "2024-03-20",
                'last_updated': "2024-03-22",
                'details': {
                    'feedback': "Application received and under review.",
                    'submitted_date': "2024-03-20"
                }
            }
        ]
        
        # Mock positions data for employers
        employer_positions = [
            {
                'id': 1,
                'employer_id': 3,  # employer1
                'name': "Software Developer Intern",
                'description': "Develop and maintain web applications using modern frameworks. Work with a team of experienced developers.",
                'capacity': 3,
                'department': "engineering",
                'endDate': "2024-06-30",
                'filled': 1,
                'created_date': "2024-02-15",
                'status': "active"
            },
            {
                'id': 2,
                'employer_id': 3,
                'name': "UI/UX Designer",
                'description': "Create intuitive and engaging user interfaces and experiences for our products.",
                'capacity': 2,
                'department': "design",
                'endDate': "2024-07-15",
                'filled': 0,
                'created_date': "2024-02-20",
                'status': "active"
            },
            {
                'id': 3,
                'employer_id': 3,
                'name': "Backend Developer",
                'description': "Build and maintain server-side logic, databases, and APIs for our applications.",
                'capacity': 2,
                'department': "engineering",
                'endDate': "2024-08-01",
                'filled': 1,
                'created_date': "2024-02-10",
                'status': "active"
            }
        ]
        
        # Mock employer applicants data
        employer_applicants = [
            {
                'id': 1,
                'position_id': 1,
                'position_name': "Software Developer Intern",
                'name': "John Smith",
                'email': "john.smith@email.com",
                'phone': "+1 (555) 123-4567",
                'applied_date': "2024-01-15",
                'status': "applied",
                'experience': "3 years",
                'education': "Bachelor's in Computer Science",
                'skills': ["React", "JavaScript", "CSS", "HTML", "Git"],
                'notes': "Strong portfolio with modern React projects. Excellent communication skills and team player."
            },
            {
                'id': 2,
                'position_id': 1,
                'position_name': "Software Developer Intern",
                'name': "Sarah Johnson",
                'email': "sarah.j@email.com",
                'phone': "+1 (555) 987-6543",
                'applied_date': "2024-01-16",
                'status': "shortlisted",
                'experience': "4 years",
                'education': "Master's in Design",
                'skills': ["Figma", "UI Design", "User Research", "Prototyping", "Wireframing"],
                'notes': "Excellent design portfolio with detailed case studies."
            },
            {
                'id': 3,
                'position_id': 2,
                'position_name': "UI/UX Designer",
                'name': "Michael Chen",
                'email': "m.chen@email.com",
                'phone': "+1 (555) 456-7890",
                'applied_date': "2024-01-14",
                'status': "accepted",
                'experience': "5 years",
                'education': "Bachelor's in Software Engineering",
                'skills': ["Node.js", "Python", "AWS", "MongoDB", "Docker"],
                'notes': "Strong backend architecture experience."
            }
        ]
        
        # Store mock data
        app.config['MOCK_USERS'] = users
        app.config['MOCK_APPLICATIONS'] = applications
        app.config['MOCK_EMPLOYER_POSITIONS'] = employer_positions
        app.config['MOCK_EMPLOYER_APPLICANTS'] = employer_applicants
        print("✓ Mock data created")
        
        # Check templates directory
        print("\n[4/4] Checking templates...")
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.exists(templates_dir):
            files = os.listdir(templates_dir)
            print(f"✓ Templates directory exists with {len(files)} files")
        else:
            print(f"✗ Templates directory NOT found: {templates_dir}")
            os.makedirs(templates_dir, exist_ok=True)
            print(f"✓ Created templates directory")
        
        # ========== ROUTES ==========
        
        @app.route('/')
        def index():
            return redirect(url_for('login_page'))
        
        @app.route('/login')
        def login_page():
            return render_template('login.html')
        
        @app.route('/dashboard')
        def dashboard_page():
            if 'user_id' not in session:
                return redirect('/login')
            
            user_type = session.get('user_type')
            
            if user_type == 'student':
                return render_template('StudentDashboard.html')
            elif user_type == 'employer':
                return render_template('EmployerDashboard.html')
            else:
                return redirect('/login')
        
        @app.route('/review')
        def review_page():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return """
            <!DOCTYPE html>
            <html>
            <head><title>Review Applicant</title><style>
                body { font-family: Arial; padding: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                .back-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 4px; margin-bottom: 20px; }
                .applicant-info { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            </style></head>
            <body>
                <div class="container">
                    <button class="back-btn" onclick="window.history.back()">← Back</button>
                    <h1>Review Applicant</h1>
                    <div class="applicant-info">
                        <h2>Applicant Details</h2>
                        <p><strong>Name:</strong> <span id="applicant-name">Loading...</span></p>
                        <p><strong>Position:</strong> <span id="applicant-position">Loading...</span></p>
                        <p><strong>Status:</strong> <span id="applicant-status">Loading...</span></p>
                        <p><strong>Applied:</strong> <span id="applicant-date">Loading...</span></p>
                        <p><strong>Experience:</strong> <span id="applicant-experience">Loading...</span></p>
                        <p><strong>Skills:</strong> <span id="applicant-skills">Loading...</span></p>
                    </div>
                    <div>
                        <button onclick="updateStatus('shortlisted')" style="background: #f39c12; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin-right: 10px;">Shortlist</button>
                        <button onclick="updateStatus('accepted')" style="background: #27ae60; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin-right: 10px;">Accept</button>
                        <button onclick="updateStatus('rejected')" style="background: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px;">Reject</button>
                    </div>
                </div>
                <script>
                    const applicantId = sessionStorage.getItem('currentApplicantId') || 1;
                    fetch(`/api/employer/applicants/${applicantId}`)
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                const app = data.applicant;
                                document.getElementById('applicant-name').textContent = app.name;
                                document.getElementById('applicant-position').textContent = app.position_name;
                                document.getElementById('applicant-status').textContent = app.status;
                                document.getElementById('applicant-date').textContent = app.applied_date;
                                document.getElementById('applicant-experience').textContent = app.experience;
                                document.getElementById('applicant-skills').textContent = app.skills ? app.skills.join(', ') : 'N/A';
                            }
                        });
                    
                    function updateStatus(newStatus) {
                        fetch(`/api/employer/applicants/${applicantId}/status`, {
                            method: 'PUT',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({ status: newStatus })
                        })
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                alert(`Status updated to ${newStatus}`);
                                document.getElementById('applicant-status').textContent = newStatus;
                            }
                        });
                    }
                </script>
            </body>
            </html>
            """
        
        # ========== AUTHENTICATION ==========
        
        @app.route('/simple_login', methods=['POST'])
        def simple_login():
            try:
                username = request.form.get('username')
                password = request.form.get('password')
                user_type = request.form.get('userType')
                
                if not username or not password:
                    return "Username and password required", 400
                
                if username not in users or users[username]['password'] != password:
                    return "Invalid credentials", 401
                
                user = users[username]
                
                if user_type and user['type'] != user_type:
                    return f"User is type {user['type']}, not {user_type}", 403
                
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_type'] = user['type']
                session.permanent = True
                
                return redirect('/dashboard')
                
            except Exception as e:
                return f"Error: {str(e)}", 500
        
        # ========== STUDENT API ==========
        
        @app.route('/api/user', methods=['GET'])
        def get_user_info():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            current_user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id:
                    current_user = user_data
                    break
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'success': True,
                'user': {
                    'id': current_user['id'],
                    'name': current_user['name'],
                    'username': current_user['username'],
                    'email': current_user['email'],
                    'type': current_user['type']
                }
            })
        
        @app.route('/api/applications', methods=['GET'])
        def get_user_applications():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user_apps = [app for app in applications if app['user_id'] == user_id]
            simplified = []
            for app in user_apps:
                simplified.append({
                    'id': app['id'],
                    'positionName': app['position_name'],
                    'company': app['company'],
                    'description': app['description'],
                    'status': app['status'],
                    'appliedDate': app['applied_date'],
                    'lastUpdated': app['last_updated']
                })
            
            return jsonify({
                'success': True,
                'applications': simplified
            })
        
        @app.route('/api/applications/<int:application_id>/response', methods=['GET'])
        def get_application_response(application_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            application = None
            for app in applications:
                if app['id'] == application_id and app['user_id'] == user_id:
                    application = app
                    break
            
            if not application:
                return jsonify({'error': 'Application not found'}), 404
            
            return jsonify({
                'success': True,
                'application': {
                    'id': application['id'],
                    'positionName': application['position_name'],
                    'company': application['company'],
                    'status': application['status'],
                    'details': application['details']
                }
            })
        
        # ========== EMPLOYER API ==========
        
        @app.route('/api/employer/user', methods=['GET'])
        def get_employer_user_info():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            current_user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    current_user = user_data
                    break
            
            if not current_user:
                return jsonify({'error': 'User not found or not employer'}), 404
            
            return jsonify({
                'success': True,
                'user': {
                    'id': current_user['id'],
                    'name': current_user['name'],
                    'username': current_user['username'],
                    'email': current_user['email'],
                    'type': current_user['type']
                }
            })
        
        @app.route('/api/employer/positions', methods=['GET'])
        def get_employer_positions():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            user_positions = [pos for pos in employer_positions if pos['employer_id'] == user_id]
            return jsonify({'success': True, 'positions': user_positions})
        
        @app.route('/api/employer/positions', methods=['POST'])
        def create_employer_position():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            data = request.get_json()
            if not data.get('name') or not data.get('description'):
                return jsonify({'error': 'Name and description required'}), 400
            
            new_id = max([p['id'] for p in employer_positions], default=0) + 1
            new_position = {
                'id': new_id,
                'employer_id': user_id,
                'name': data.get('name'),
                'description': data.get('description'),
                'capacity': data.get('capacity', 1),
                'department': data.get('department', 'engineering'),
                'endDate': data.get('endDate'),
                'filled': 0,
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'active'
            }
            
            employer_positions.append(new_position)
            return jsonify({'success': True, 'position': new_position})
        
        @app.route('/api/employer/positions/<int:position_id>', methods=['PUT'])
        def update_employer_position(position_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            data = request.get_json()
            position_index = None
            
            for i, pos in enumerate(employer_positions):
                if pos['id'] == position_id and pos['employer_id'] == user_id:
                    position_index = i
                    break
            
            if position_index is None:
                return jsonify({'error': 'Position not found'}), 404
            
            employer_positions[position_index].update({
                'name': data.get('name', employer_positions[position_index]['name']),
                'description': data.get('description', employer_positions[position_index]['description']),
                'capacity': data.get('capacity', employer_positions[position_index]['capacity']),
                'department': data.get('department', employer_positions[position_index]['department']),
                'endDate': data.get('endDate', employer_positions[position_index]['endDate'])
            })
            
            return jsonify({'success': True, 'position': employer_positions[position_index]})
        
        @app.route('/api/employer/positions/<int:position_id>', methods=['DELETE'])
        def delete_employer_position(position_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            position_index = None
            for i, pos in enumerate(employer_positions):
                if pos['id'] == position_id and pos['employer_id'] == user_id:
                    position_index = i
                    break
            
            if position_index is None:
                return jsonify({'error': 'Position not found'}), 404
            
            deleted = employer_positions.pop(position_index)
            return jsonify({'success': True, 'message': 'Position deleted', 'position': deleted})
        
        @app.route('/api/employer/applicants', methods=['GET'])
        def get_employer_applicants():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            position_ids = [pos['id'] for pos in employer_positions if pos['employer_id'] == user_id]
            user_apps = [app for app in employer_applicants if app['position_id'] in position_ids]
            return jsonify({'success': True, 'applicants': user_apps})
        
        @app.route('/api/employer/applicants/<int:applicant_id>', methods=['GET'])
        def get_employer_applicant(applicant_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            applicant = None
            for app in employer_applicants:
                if app['id'] == applicant_id:
                    position = next((p for p in employer_positions if p['id'] == app['position_id'] and p['employer_id'] == user_id), None)
                    if position:
                        applicant = app
                    break
            
            if not applicant:
                return jsonify({'error': 'Applicant not found'}), 404
            
            return jsonify({'success': True, 'applicant': applicant})
        
        @app.route('/api/employer/applicants/<int:applicant_id>/status', methods=['PUT'])
        def update_applicant_status(applicant_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not employer'}), 403
            
            data = request.get_json()
            new_status = data.get('status')
            if not new_status:
                return jsonify({'error': 'Status required'}), 400
            
            applicant_index = None
            for i, app in enumerate(employer_applicants):
                if app['id'] == applicant_id:
                    position = next((p for p in employer_positions if p['id'] == app['position_id'] and p['employer_id'] == user_id), None)
                    if position:
                        applicant_index = i
                    break
            
            if applicant_index is None:
                return jsonify({'error': 'Applicant not found'}), 404
            
            employer_applicants[applicant_index]['status'] = new_status
            return jsonify({'success': True, 'applicant': employer_applicants[applicant_index]})
        
        # ========== UTILITY ROUTES ==========
        
        @app.route('/api/auth/login', methods=['POST'])
        def api_login():
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
                
                if username not in users or users[username]['password'] != password:
                    return jsonify({'error': 'Invalid credentials'}), 401
                
                user = users[username]
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_type'] = user['type']
                session.permanent = True
                
                access_token = create_access_token(identity={
                    'id': user['id'],
                    'username': user['username'],
                    'name': user['name'],
                    'type': user['type']
                })
                
                return jsonify({
                    'success': True,
                    'token': access_token,
                    'user': user
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @app.route('/health')
        def health_check():
            return jsonify({'status': 'ok'})
        
        @app.route('/test')
        def test():
            return "Flask is working!"
        
        @app.route('/logout')
        def logout():
            session.clear()
            return redirect('/login')
        
        print("✓ All routes configured")
        
        # Startup message
        print("\n" + "=" * 50)
        print("Flask Internship Platform - READY")
        print("=" * 50)
        print("\nAvailable URLs:")
        print("  • http://localhost:5000/              - Home (redirects to login)")
        print("  • http://localhost:5000/login         - Login page")
        print("  • http://localhost:5000/dashboard     - Dashboard (auto-detects user type)")
        print("  • http://localhost:5000/review        - Applicant review page (employers only)")
        print("  • http://localhost:5000/test          - Test page")
        print("  • http://localhost:5000/health        - Health check")
        print("\nDemo credentials:")
        print("  • Students: johndoe / password123")
        print("  • Employers: employer1 / password123")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start server
        app.run(debug=True, port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"\n✗ IMPORT ERROR: {e}")
        print("\nInstall missing dependencies:")
        print("  pip install flask flask-jwt-extended flask-cors python-dotenv")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())