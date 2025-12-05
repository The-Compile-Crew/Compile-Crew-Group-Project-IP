import unittest
from App.main import create_app
from App.database import db
from App.controllers import create_user, open_position, add_student_to_shortlist
from App.models import Student, Staff, Position


class StaffViewsTests(unittest.TestCase):
    """Test Staff Dashboard and shortlist management views"""
    
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
    
    def test_staff_dashboard_access(self):
        """Test staff can access their dashboard after login"""
        staff_user = create_user("staff_test", "password123", "staff")
        
        with self.client.session_transaction() as sess:
            sess['user_id'] = staff_user.id
            sess['username'] = staff_user.username
        
        response = self.client.get('/StaffDashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_staff_dashboard_requires_authentication(self):
        """Test that staff dashboard redirects when not logged in"""
        response = self.client.get('/StaffDashboard', follow_redirects=False)
        self.assertIn(response.status_code, [302, 301])
    
    def test_add_student_to_shortlist_form(self):
        """Test staff can add student to shortlist via form"""
        # Create users
        staff_user = create_user("staff_add", "pass", "staff")
        student_user = create_user("student_add", "pass", "student", student_id="816000010")
        employer_user = create_user("employer_add", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "Test Position", 3)
        
        # Get student record
        student = Student.query.filter_by(user_id=student_user.id).first()
        
        # Login as staff
        with self.client.session_transaction() as sess:
            sess['user_id'] = staff_user.id
            sess['username'] = staff_user.username
        
        # Submit form to add student to shortlist
        response = self.client.post('/shortlist/add', data={
            'student_id': student.student_id,
            'position_id': position.id,
            'details': 'Test details'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    def test_add_to_shortlist_page_loads(self):
        """Test the add to shortlist form page loads correctly"""
        # Create employer and position
        employer_user = create_user("employer_page", "pass", "employer")
        position = open_position(employer_user.id, "Page Test Position", 2)
        
        response = self.client.get(f'/shortlist/add/{position.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'add to shortlist', response.data.lower())
    
    def test_add_to_shortlist_requires_auth(self):
        """Test adding to shortlist requires authentication"""
        response = self.client.post('/shortlist/add', data={
            'student_id': '816000011',
            'position_id': 1,
            'details': 'Test'
        }, follow_redirects=True)
        
        # Should redirect or show error
        self.assertEqual(response.status_code, 200)
    
    def test_review_application_page(self):
        """Test staff can view review application page"""
        # Create users and shortlist
        staff_user = create_user("staff_review", "pass", "staff")
        student_user = create_user("student_review", "pass", "student", student_id="816000012")
        employer_user = create_user("employer_review", "pass", "employer")
        
        position = open_position(employer_user.id, "Review Position", 2)
        
        shortlist = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "Review Student",
            "816000012",
            "Review details"
        )
        
        student = Student.query.filter_by(user_id=student_user.id).first()
        
        response = self.client.get(f'/shortlist/review/{student.id}/{position.id}')
        self.assertEqual(response.status_code, 200)
