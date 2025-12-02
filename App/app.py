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
            },
            {
                'id': 4,
                'employer_id': 4,  # employer2
                'name': "Data Analyst",
                'description': "Analyze complex data sets to provide insights and support data-driven decision making.",
                'capacity': 2,
                'department': "engineering",
                'endDate': "2024-09-30",
                'filled': 0,
                'created_date': "2024-02-25",
                'status': "active"
            }
        ]
        
        # Mock employer applicants data
        employer_applicants = [
            {
                'id': 1,
                'position_id': 1,  # Software Developer Intern
                'position_name': "Software Developer Intern",
                'name': "John Smith",
                'email': "john.smith@email.com",
                'phone': "+1 (555) 123-4567",
                'applied_date': "2024-01-15",
                'status': "applied",
                'experience': "3 years",
                'education': "Bachelor's in Computer Science",
                'skills': ["React", "JavaScript", "CSS", "HTML", "Git"],
                'notes': "Strong portfolio with modern React projects. Excellent communication skills and team player.",
                'resume_url': "/resumes/john_smith.pdf"
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
                'notes': "Excellent design portfolio with detailed case studies.",
                'resume_url': "/resumes/sarah_johnson.pdf"
            },
            {
                'id': 3,
                'position_id': 2,  # UI/UX Designer
                'position_name': "UI/UX Designer",
                'name': "Michael Chen",
                'email': "m.chen@email.com",
                'phone': "+1 (555) 456-7890",
                'applied_date': "2024-01-14",
                'status': "accepted",
                'experience': "5 years",
                'education': "Bachelor's in Software Engineering",
                'skills': ["Node.js", "Python", "AWS", "MongoDB", "Docker"],
                'notes': "Strong backend architecture experience.",
                'resume_url': "/resumes/michael_chen.pdf"
            },
            {
                'id': 4,
                'position_id': 2,
                'position_name': "UI/UX Designer",
                'name': "Emily Davis",
                'email': "emily.davis@email.com",
                'phone': "+1 (555) 234-5678",
                'applied_date': "2024-01-17",
                'status': "rejected",
                'experience': "6 years",
                'education': "MBA",
                'skills': ["Product Strategy", "Agile", "Analytics", "Roadmapping"],
                'notes': "Good overall experience but lacks specific industry knowledge.",
                'resume_url': "/resumes/emily_davis.pdf"
            },
            {
                'id': 5,
                'position_id': 3,  # Backend Developer
                'position_name': "Backend Developer",
                'name': "Robert Wilson",
                'email': "robert.wilson@email.com",
                'phone': "+1 (555) 345-6789",
                'applied_date': "2024-01-18",
                'status': "applied",
                'experience': "2 years",
                'education': "Bachelor's in Statistics",
                'skills': ["SQL", "Python", "Tableau", "Excel", "R"],
                'notes': "Strong analytical skills with good attention to detail.",
                'resume_url': "/resumes/robert_wilson.pdf"
            }
        ]
        
        # Store mock data in app config
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
            for file in files:
                print(f"  • {file}")
        else:
            print(f"✗ Templates directory NOT found: {templates_dir}")
            os.makedirs(templates_dir, exist_ok=True)
            print(f"✓ Created templates directory")
        
        # Routes
        print("\n" + "=" * 50)
        print("Setting up routes...")
        
        # ========== PAGES ==========
        
        @app.route('/')
        def index():
            return redirect(url_for('login_page'))
        
        @app.route('/login')
        def login_page():
            print(f"  → Serving /login")
            return render_template('login.html')
        
        @app.route('/dashboard')
        def dashboard_page():
            # Check if user is logged in
            if 'user_id' not in session:
                print(f"  → User not logged in, redirecting to login")
                return redirect('/login')
            
            user_id = session.get('user_id')
            user_type = session.get('user_type')
            
            print(f"  → Serving /dashboard for user {user_id} (type: {user_type})")
            
            if user_type == 'student':
                return render_template('StudentDashboard.html')
            elif user_type == 'employer':
                return render_template('Employer dashboard.html')
            else:
                return redirect('/login')
        
        @app.route('/review')
        def review_page():
            # Check if user is logged in as employer
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            
            print(f"  → Serving /review for employer {session.get('user_id')}")
            # For now, return a simple page - you can create a review.html template later
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Review Applicant</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .back-btn { 
                        background-color: #3498db; 
                        color: white; 
                        border: none; 
                        padding: 10px 20px; 
                        border-radius: 4px; 
                        cursor: pointer; 
                        margin-bottom: 20px;
                    }
                    .applicant-info { 
                        background-color: #f8f9fa; 
                        padding: 20px; 
                        border-radius: 8px; 
                        margin-bottom: 20px; 
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <button class="back-btn" onclick="window.history.back()">← Back to Dashboard</button>
                    <h1>Applicant Review Page</h1>
                    <div class="applicant-info">
                        <h2>Applicant Details</h2>
                        <p><strong>Name:</strong> <span id="applicant-name">Loading...</span></p>
                        <p><strong>Position:</strong> <span id="applicant-position">Loading...</span></p>
                        <p><strong>Status:</strong> <span id="applicant-status">Loading...</span></p>
                        <p><strong>Applied Date:</strong> <span id="applicant-date">Loading...</span></p>
                        <p><strong>Experience:</strong> <span id="applicant-experience">Loading...</span></p>
                        <p><strong>Education:</strong> <span id="applicant-education">Loading...</span></p>
                        <p><strong>Skills:</strong> <span id="applicant-skills">Loading...</span></p>
                        <p><strong>Notes:</strong> <span id="applicant-notes">Loading...</span></p>
                    </div>
                    <div>
                        <button onclick="updateStatus('shortlisted')" style="background-color: #f39c12; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin-right: 10px;">Shortlist</button>
                        <button onclick="updateStatus('accepted')" style="background-color: #27ae60; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin-right: 10px;">Accept</button>
                        <button onclick="updateStatus('rejected')" style="background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 4px;">Reject</button>
                    </div>
                </div>
                <script>
                    // Get applicant ID from sessionStorage (set by EmployerDashboard)
                    const applicantId = sessionStorage.getItem('currentApplicantId') || 1;
                    
                    // Fetch applicant details
                    fetch(`/api/employer/applicants/${applicantId}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.success && data.applicant) {
                                const app = data.applicant;
                                document.getElementById('applicant-name').textContent = app.name;
                                document.getElementById('applicant-position').textContent = app.position_name;
                                document.getElementById('applicant-status').textContent = app.status;
                                document.getElementById('applicant-date').textContent = app.applied_date;
                                document.getElementById('applicant-experience').textContent = app.experience;
                                document.getElementById('applicant-education').textContent = app.education;
                                document.getElementById('applicant-skills').textContent = app.skills ? app.skills.join(', ') : 'N/A';
                                document.getElementById('applicant-notes').textContent = app.notes || 'No notes';
                            }
                        })
                        .catch(error => {
                            console.error('Error loading applicant:', error);
                            document.getElementById('applicant-name').textContent = 'Error loading data';
                        });
                    
                    function updateStatus(newStatus) {
                        fetch(`/api/employer/applicants/${applicantId}/status`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ status: newStatus })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert(`Applicant status updated to ${newStatus}`);
                                document.getElementById('applicant-status').textContent = newStatus;
                            } else {
                                alert('Failed to update status');
                            }
                        })
                        .catch(error => {
                            console.error('Error updating status:', error);
                            alert('Error updating status');
                        });
                    }
                </script>
            </body>
            </html>
            """
        
        # ========== AUTHENTICATION ==========
        
        @app.route('/simple_login', methods=['POST', 'GET'])
        def simple_login():
            try:
                if request.method == 'GET':
                    return "GET method not allowed for login. Use POST.", 405
                
                print("=== DEBUG: Form Data Received ===")
                print(f"Form data: {request.form}")
                print(f"Username: {request.form.get('username')}")
                print(f"Password: {request.form.get('password')}")
                print(f"User Type: {request.form.get('userType')}")
                
                # Get form data
                username = request.form.get('username')
                password = request.form.get('password')
                user_type = request.form.get('userType')
                
                if not username or not password:
                    return "Username and password are required", 400
                
                # Find user in mock data
                if username not in users or users[username]['password'] != password:
                    return f"Invalid username or password. Try: johndoe / password123", 401
                
                user = users[username]
                
                # Check user type if specified
                if user_type and user['type'] != user_type:
                    return f"Access denied. User '{username}' is type '{user['type']}', not '{user_type}'", 403
                
                # Store user in session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_type'] = user['type']
                session.permanent = True
                
                print(f"=== DEBUG: Login successful for user {user['id']}, redirecting to dashboard ===")
                return redirect('/dashboard')
                
            except Exception as e:
                print(f"=== DEBUG: Error in simple_login: {e}")
                import traceback
                traceback.print_exc()
                return f"Internal server error: {str(e)}", 500
        
        # ========== STUDENT API ENDPOINTS ==========
        
        @app.route('/api/user', methods=['GET'])
        def get_user_info():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Find the current user
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
            
            user_applications = [
                app for app in applications if app['user_id'] == user_id
            ]
            
            simplified = []
            for app in user_applications:
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
        
        # ========== EMPLOYER API ENDPOINTS ==========
        
        @app.route('/api/employer/user', methods=['GET'])
        def get_employer_user_info():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Find the current user
            current_user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    current_user = user_data
                    break
            
            if not current_user:
                return jsonify({'error': 'User not found or not an employer'}), 404
            
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
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            user_positions = [
                pos for pos in employer_positions if pos['employer_id'] == user_id
            ]
            
            return jsonify({
                'success': True,
                'positions': user_positions
            })
        
        @app.route('/api/employer/positions', methods=['POST'])
        def create_employer_position():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            data = request.get_json()
            
            # Validate required fields
            if not data.get('name') or not data.get('description'):
                return jsonify({'error': 'Name and description are required'}), 400
            
            # Generate new ID
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
            
            return jsonify({
                'success': True,
                'position': new_position
            })
        
        @app.route('/api/employer/positions/<int:position_id>', methods=['PUT'])
        def update_employer_position(position_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            data = request.get_json()
            
            # Find position
            position_index = None
            for i, pos in enumerate(employer_positions):
                if pos['id'] == position_id and pos['employer_id'] == user_id:
                    position_index = i
                    break
            
            if position_index is None:
                return jsonify({'error': 'Position not found'}), 404
            
            # Update position
            employer_positions[position_index].update({
                'name': data.get('name', employer_positions[position_index]['name']),
                'description': data.get('description', employer_positions[position_index]['description']),
                'capacity': data.get('capacity', employer_positions[position_index]['capacity']),
                'department': data.get('department', employer_positions[position_index]['department']),
                'endDate': data.get('endDate', employer_positions[position_index]['endDate'])
            })
            
            return jsonify({
                'success': True,
                'position': employer_positions[position_index]
            })
        
        @app.route('/api/employer/positions/<int:position_id>', methods=['DELETE'])
        def delete_employer_position(position_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            # Find position
            position_index = None
            for i, pos in enumerate(employer_positions):
                if pos['id'] == position_id and pos['employer_id'] == user_id:
                    position_index = i
                    break
            
            if position_index is None:
                return jsonify({'error': 'Position not found'}), 404
            
            # Remove position
            deleted_position = employer_positions.pop(position_index)
            
            return jsonify({
                'success': True,
                'message': 'Position deleted successfully',
                'position': deleted_position
            })
        
        @app.route('/api/employer/applicants', methods=['GET'])
        def get_employer_applicants():
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            # Get positions for this employer
            employer_position_ids = [pos['id'] for pos in employer_positions if pos['employer_id'] == user_id]
            
            # Get applicants for these positions
            user_applicants = [
                app for app in employer_applicants if app['position_id'] in employer_position_ids
            ]
            
            return jsonify({
                'success': True,
                'applicants': user_applicants
            })
        
        @app.route('/api/employer/applicants/<int:applicant_id>', methods=['GET'])
        def get_employer_applicant(applicant_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            # Find applicant
            applicant = None
            for app in employer_applicants:
                if app['id'] == applicant_id:
                    # Check if this applicant belongs to one of the employer's positions
                    position = next((p for p in employer_positions if p['id'] == app['position_id'] and p['employer_id'] == user_id), None)
                    if position:
                        applicant = app
                    break
            
            if not applicant:
                return jsonify({'error': 'Applicant not found'}), 404
            
            return jsonify({
                'success': True,
                'applicant': applicant
            })
        
        @app.route('/api/employer/applicants/<int:applicant_id>/status', methods=['PUT'])
        def update_applicant_status(applicant_id):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Not authenticated'}), 401
            
            # Verify user is an employer
            user = None
            for username, user_data in users.items():
                if user_data['id'] == user_id and user_data['type'] == 'employer':
                    user = user_data
                    break
            
            if not user:
                return jsonify({'error': 'User is not an employer'}), 403
            
            data = request.get_json()
            new_status = data.get('status')
            
            if not new_status:
                return jsonify({'error': 'Status is required'}), 400
            
            # Find applicant
            applicant_index = None
            for i, app in enumerate(employer_applicants):
                if app['id'] == applicant_id:
                    # Check if this applicant belongs to one of the employer's positions
                    position = next((p for p in employer_positions if p['id'] == app['position_id'] and p['employer_id'] == user_id), None)
                    if position:
                        applicant_index = i
                    break
            
            if applicant_index is None:
                return jsonify({'error': 'Applicant not found'}), 404
            
            # Update status
            employer_applicants[applicant_index]['status'] = new_status
            
            return jsonify({
                'success': True,
                'applicant': employer_applicants[applicant_index]
            })
        
        # ========== OTHER ENDPOINTS ==========
        
        @app.route('/api/auth/login', methods=['POST'])
        def api_login():
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
                
                if username not in users or users[username]['password'] != password:
                    return jsonify({'error': 'Invalid credentials'}), 401
                
                user = users[username]
                
                # Also set session for consistency
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
        print("  • Students:")
        print("      Username: johndoe")
        print("      Password: password123")
        print("      User Type: student")
        print("  • Employers:")
        print("      Username: employer1")
        print("      Password: password123")
        print("      User Type: employer")
        print("\nAPI Endpoints:")
        print("  • GET /api/user                       - Get current user info")
        print("  • GET /api/applications               - Get user applications (students)")
        print("  • GET /api/applications/:id/response  - Get application response")
        print("  • GET /api/employer/user              - Get employer user info")
        print("  • GET /api/employer/positions         - Get employer positions")
        print("  • POST /api/employer/positions        - Create new position")
        print("  • PUT /api/employer/positions/:id     - Update position")
        print("  • DELETE /api/employer/positions/:id  - Delete position")
        print("  • GET /api/employer/applicants        - Get employer applicants")
        print("  • GET /api/employer/applicants/:id    - Get specific applicant")
        print("  • PUT /api/employer/applicants/:id/status - Update applicant status")
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