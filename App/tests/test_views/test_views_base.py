import unittest
from App.main import create_app
from App.database import db
from App.controllers import create_user, open_position


class ViewsIntegrationTests(unittest.TestCase):
    """Test Flask routes and views"""
    
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index_shows_login_page(self):
        """Test that index shows login page"""
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())
    
    def test_health_check(self):
        """Test that health check endpoint works"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data.lower())
    
    def test_student_dashboard_requires_authentication(self):
        """Test that student dashboard redirects when not logged in"""
        response = self.client.get('/student-dashboard', follow_redirects=False)
        # Should redirect to login page
        self.assertIn(response.status_code, [302, 301])
    
    def test_login_workflow(self):
        """Test login POST request"""
        # Create a test user
        create_user("testuser", "testpass", "student", student_id="816000001")
        
        # Attempt login with correct userType field name
        response = self.client.post('/simple_login', data={
            'username': 'testuser',
            'password': 'testpass',
            'userType': 'student'  # Match the form field name
        }, follow_redirects=True)
        
        # Should redirect to dashboard after successful login
        self.assertEqual(response.status_code, 200)
    
    def test_student_dashboard_access(self):
        """Test student can access their dashboard after login"""
        # Create student
        student = create_user("student1", "password123", "student", student_id="816000002")
        
        # Login
        with self.client.session_transaction() as sess:
            sess['user_id'] = student.id
            sess['username'] = student.username
        
        response = self.client.get('/student-dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_employer_dashboard_access(self):
        """Test employer can access their dashboard after login"""
        # Create employer
        employer = create_user("employer1", "password123", "employer")
        
        # Login
        with self.client.session_transaction() as sess:
            sess['user_id'] = employer.id
            sess['username'] = employer.username
        
        response = self.client.get('/employerdashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_logout_clears_session(self):
        """Test that logout clears session data"""
        # Create and login user
        user = create_user("logouttest", "password123", "student", student_id="816000003")
        
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['username'] = user.username
        
        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Session should be cleared
        with self.client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)
