        # ...existing code...
import sys
import traceback
from datetime import datetime
import sqlite3
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-12345')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
CORS(app, supports_credentials=True)
jwt = JWTManager(app)

def get_db():
    if not hasattr(app, 'db_conn'):
        app.db_conn = sqlite3.connect('App/appdata.db', check_same_thread=False)
        app.db_conn.row_factory = sqlite3.Row
    return app.db_conn

def init_db():
    db = get_db()
    with open('App/schema.sql', 'r') as f:
        db.executescript(f.read())
init_db()

@app.route('/staff/addtoshortlist', methods=['GET', 'POST'])
def staff_add_to_shortlist():
    if 'user_id' not in session or session.get('user_type') != 'staff':
        return redirect('/login')
    db = get_db()
    if request.method == 'POST':
        position_id = request.form.get('position_id', 1)
        student_id = request.form.get('student_id') or request.form.get('student_user_id')
        student_name = request.form.get('student_name') or request.form.get('name')
        email = request.form.get('email')
        details = request.form.get('details')
        db.execute('INSERT INTO applicants (name, email, student_id, details, position_id, status, applied_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (student_name, email, student_id, details, position_id, 'shortlisted', datetime.now().strftime('%Y-%m-%d')))
        db.commit()
        return redirect('/dashboard')
    # GET: Render form
    students = [dict(row) for row in db.execute('SELECT * FROM users WHERE type = "student"').fetchall()]
    position_id = request.args.get('position_id', 1)
    return render_template('addtoshortlist.html', students=students, position_id=position_id)

print("=" * 50)
print("Starting Flask Internship Platform")
print("=" * 50)

def main():
    try:
        # Mock user data
        users = {
            1: {'username':'staff',
                'password': 'password123',
                'name': 'Admin Staff',
                'email': 'staff@example.com',
                'type': 'staff'}
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
        
        # Initialize shortlist storage (position_id -> list of applicant_ids)
        app.config['STAFF_SHORTLIST'] = {}
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
            user_id = session.get('user_id')
            
            if user_type == 'student':
                # Get student's applications
                student_applications = [application for application in app.config['MOCK_APPLICATIONS'] if application['user_id'] == user_id]
                # Also get all available positions for students to view
                all_positions = app.config['MOCK_EMPLOYER_POSITIONS']
                
                # Search filter for positions
                search_query = request.args.get('search', '').lower()
                if search_query:
                    all_positions = [pos for pos in all_positions 
                                   if search_query in pos['name'].lower() or search_query in pos['description'].lower()]
                
                return render_template('StudentDashboard.html', applications=student_applications, positions=all_positions, search_query=search_query)
            
            elif user_type == 'employer':
                db = get_db()
                # Get employer's positions (still mock for now)
                employer_positions = [pos for pos in app.config['MOCK_EMPLOYER_POSITIONS'] if pos['employer_id'] == user_id]
                search_query = request.args.get('search', '').lower()
                if search_query:
                    employer_positions = [pos for pos in employer_positions 
                                        if search_query in pos['name'].lower() or search_query in pos['description'].lower()]
                position_ids = [pos['id'] for pos in employer_positions]
                placeholders = ','.join(['?']*len(position_ids)) if position_ids else 'NULL'
                query = f'SELECT * FROM applicants WHERE position_id IN ({placeholders})' if position_ids else 'SELECT * FROM applicants WHERE 0'
                employer_applicants = [dict(row) for row in db.execute(query, position_ids).fetchall()] if position_ids else []
                applicant_search = request.args.get('applicant_search', '').lower()
                if applicant_search:
                    employer_applicants = [a for a in employer_applicants 
                                          if applicant_search in a['name'].lower() or applicant_search in a['email'].lower()]
                return render_template('EmployerDashboard.html', 
                                     positions=employer_positions,
                                     applicants=employer_applicants,
                                     search_query=search_query)
            
            elif user_type == 'staff':
                # Staff can see all positions and applicants
                all_positions = app.config['MOCK_EMPLOYER_POSITIONS']
                all_applicants = app.config['MOCK_EMPLOYER_APPLICANTS']
                
                # Search filters
                search_query = request.args.get('search', '').lower()
                if search_query:
                    all_positions = [pos for pos in all_positions 
                                   if search_query in pos['name'].lower() or search_query in pos['description'].lower()]
                
                applicant_search = request.args.get('applicant_search', '').lower()
                if applicant_search:
                    all_applicants = [a for a in all_applicants 
                                     if applicant_search in a['name'].lower() or applicant_search in a['email'].lower()]
                
                return render_template('StaffDashboard.html', 
                                     positions=all_positions,
                                     applicants=all_applicants,
                                     search_query=search_query)
            
            else:
                return redirect('/login')
        
        @app.route('/review')
        def review_page():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            
            # Get applicant ID from query parameter
            applicant_id = request.args.get('id', 1, type=int)
            
            # Find the applicant in mock data
            applicant = None
            for applicant_data in app.config['MOCK_EMPLOYER_APPLICANTS']:
                if applicant_data['id'] == applicant_id:
                    applicant = applicant_data
                    break
            
            if not applicant:
                # Use first applicant as default
                if app.config['MOCK_EMPLOYER_APPLICANTS']:
                    applicant = app.config['MOCK_EMPLOYER_APPLICANTS'][0]
                else:
                    # Return a page with no applicant data
                    applicant = {
                        'name': 'No applicants',
                        'position_name': 'N/A',
                        'status': 'N/A',
                        'applied_date': 'N/A',
                        'experience': 'N/A',
                        'skills': [],
                        'email': 'N/A',
                        'phone': 'N/A',
                        'education': 'N/A'
                    }
            
            return render_template('review.html', applicant=applicant)
        
        # ========== AUTHENTICATION ==========
        
        @app.route('/simple_login', methods=['POST'])
        def simple_login():
            try:
                db = get_db()
                username = request.form.get('username')
                password = request.form.get('password')
                user_type = request.form.get('userType') or request.form.get('user_type')

                if not username or not password:
                    return "Username and password required", 400

                cur = db.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchone()
                if not user or user['password'] != password:
                    return "Invalid credentials", 401

                if user_type and user['type'] != user_type:
                    return f"User is type {user['type']}, not {user_type}", 403

                session['user_id'] = user['id']
                session['username'] = user['username']
                session['user_type'] = user['type']
                session.permanent = True

                # Redirect to dashboard (handles user type automatically)
                return redirect('/dashboard')

            except Exception as e:
                return f"Error: {str(e)}", 500
        
        # ========== API ROUTES DISABLED FOR UI-ONLY MODE ==========
        # All /api/* endpoints below have been redirected to server-rendered pages
        
        @app.route('/api/user', methods=['GET'])
        def get_user_info():
            if 'user_id' not in session:
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/applications', methods=['GET'])
        def get_user_applications():
            if 'user_id' not in session:
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/applications/<int:application_id>/response', methods=['GET'])
        def get_application_response(application_id):
            if 'user_id' not in session:
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/employer/user', methods=['GET'])
        def get_employer_user_info():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/employer/positions', methods=['GET', 'POST'])
        def get_employer_positions():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/employer/positions/<int:position_id>', methods=['PUT', 'DELETE'])
        def update_delete_employer_position(position_id):
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/employer/applicants', methods=['GET'])
        def get_employer_applicants():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/employer/applicants/<int:applicant_id>', methods=['GET'])
        def get_employer_applicant(applicant_id):
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/employer/applicants/<int:applicant_id>/status', methods=['PUT'])
        def update_applicant_status(applicant_id):
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            return redirect('/dashboard')
        
        @app.route('/api/auth/login', methods=['POST'])
        def api_login():
            # Legacy API login removed for UI-only mode; use /simple_login form instead
            return redirect('/login')
        
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
        
        # ========== SERVER-RENDERED POSITION PAGES ==========
        
        @app.route('/positions/create', methods=['GET', 'POST'])
        def create_position_page():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            
            if request.method == 'POST':
                # Handle form submission
                try:
                    title = request.form.get('title')
                    description = request.form.get('description')
                    capacity = request.form.get('capacity')
                    end_date = request.form.get('end_date')
                    
                    if not title or not description or not capacity:
                        return "All fields are required", 400
                    
                    # Mock: Add position to the mock data
                    new_position = {
                        'id': len(app.config['MOCK_EMPLOYER_POSITIONS']) + 1,
                        'employer_id': session['user_id'],
                        'name': title,
                        'description': description,
                        'capacity': int(capacity),
                        'department': 'general',
                        'endDate': end_date or '2024-12-31',
                        'filled': 0,
                        'created_date': datetime.now().strftime('%Y-%m-%d'),
                        'status': 'active'
                    }
                    app.config['MOCK_EMPLOYER_POSITIONS'].append(new_position)
                    
                    return redirect('/dashboard')
                except Exception as e:
                    return f"Error creating position: {str(e)}", 500
            
            return render_template('positions/create.html')
        
        @app.route('/positions/<int:position_id>/edit', methods=['GET', 'POST'])
        def edit_position_page(position_id):
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            
            if request.method == 'POST':
                # Handle form submission for edit
                try:
                    title = request.form.get('title')
                    description = request.form.get('description')
                    capacity = request.form.get('capacity')
                    end_date = request.form.get('end_date')
                    
                    if not title or not description or not capacity:
                        return "All fields are required", 400
                    
                    # Mock: Update position in mock data
                    for position in app.config['MOCK_EMPLOYER_POSITIONS']:
                        if position['id'] == position_id:
                            position['name'] = title
                            position['description'] = description
                            position['capacity'] = int(capacity)
                            position['endDate'] = end_date or position['endDate']
                            break
                    
                    return redirect('/dashboard')
                except Exception as e:
                    return f"Error updating position: {str(e)}", 500
            
            # Find and display the position
            position = None
            for pos in app.config['MOCK_EMPLOYER_POSITIONS']:
                if pos['id'] == position_id:
                    position = pos
                    break
            
            if not position:
                return "Position not found", 404
            
            return render_template('positions/edit.html', position=position)
        
        # ========== SHORTLIST ROUTES ==========
        
        
        @app.route('/staff/shortlist/<int:position_id>', methods=['GET'])
        def get_staff_shortlist(position_id):
            if 'user_id' not in session or session.get('user_type') != 'staff':
                return redirect('/login')
            
            try:
                # Get applicants in this position's shortlist
                shortlist_applicant_ids = app.config['STAFF_SHORTLIST'].get(position_id, [])
                
                # Get position details
                position = None
                for pos in app.config['MOCK_EMPLOYER_POSITIONS']:
                    if pos['id'] == position_id:
                        position = pos
                        break
                
                # Get full applicant details for shortlisted applicants
                shortlisted_applicants = []
                for applicant in app.config['MOCK_EMPLOYER_APPLICANTS']:
                    if applicant['id'] in shortlist_applicant_ids:
                        shortlisted_applicants.append(applicant)
                
                return render_template('staff/shortlist.html', 
                                     position=position,
                                     shortlisted_applicants=shortlisted_applicants,
                                     position_id=position_id,
                                     students=[u for u in app.config['MOCK_USERS'].values() if u['type'] == 'student'])
            except Exception as e:
                print(f"Error getting shortlist: {str(e)}")
                return f"Error getting shortlist: {str(e)}", 500
        
        @app.route('/staff/shortlist/<int:position_id>/remove/<int:applicant_id>', methods=['POST'])
        def remove_from_shortlist(position_id, applicant_id):
            if 'user_id' not in session or session.get('user_type') != 'staff':
                return redirect('/login')
            
            try:
                if position_id in app.config['STAFF_SHORTLIST']:
                    if applicant_id in app.config['STAFF_SHORTLIST'][position_id]:
                        app.config['STAFF_SHORTLIST'][position_id].remove(applicant_id)
                
                return redirect(f'/staff/shortlist/{position_id}')
            except Exception as e:
                print(f"Error removing from shortlist: {str(e)}")
                return f"Error removing from shortlist: {str(e)}", 500
        
        @app.route('/shortlist/add', methods=['POST'])
        def add_to_shortlist():
            if 'user_id' not in session or session.get('user_type') != 'employer':
                return redirect('/login')
            
            try:
                position_id = request.form.get('position_id')
                student_id = request.form.get('student_id')
                student_name = request.form.get('student_name')
                details = request.form.get('details')
                
                # Mock: Add to shortlist (in real app, would save to database)
                shortlist_entry = {
                    'position_id': int(position_id),
                    'student_id': student_id,
                    'student_name': student_name,
                    'details': details,
                    'status': 'pending'
                }
                app.config['MOCK_EMPLOYER_APPLICANTS'].append(shortlist_entry)
                
                return redirect('/dashboard')
            except Exception as e:
                return f"Error adding to shortlist: {str(e)}", 500
        
        @app.route('/simple_signup', methods=['POST'])
        def simple_signup():
            try:
                db = get_db()
                username = request.form.get('username')
                password = request.form.get('password')
                user_type = request.form.get('user_type')
                email = request.form.get('email')
                if not username or not password or not user_type:
                    return "All fields are required", 400
                cur = db.execute('SELECT id FROM users WHERE username = ?', (username,))
                if cur.fetchone():
                    return "Username already exists", 400
                db.execute('INSERT INTO users (username, password, email, type) VALUES (?, ?, ?, ?)',
                           (username, password, email, user_type))
                db.commit()
                return redirect('/login')
            except Exception as e:
                return f"Error creating account: {str(e)}", 500
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