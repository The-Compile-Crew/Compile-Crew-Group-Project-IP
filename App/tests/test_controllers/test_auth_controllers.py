import unittest
from App.controllers import create_user
from App.models import User
from App.database import db
from App.main import create_app


class AuthControllerUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_authentication_valid_password(self):
        """Test that user can authenticate with valid credentials"""
        user = create_user("john_student", "password123", "student")
        self.assertIsNotNone(user)
        
        # Check password manually
        found_user = User.query.filter_by(username="john_student").first()
        self.assertIsNotNone(found_user)
        self.assertTrue(found_user.check_password("password123"))
    
    def test_user_authentication_invalid_password(self):
        """Test that authentication fails with wrong password"""
        user = create_user("test_user", "correctpass", "student")
        
        found_user = User.query.filter_by(username="test_user").first()
        self.assertFalse(found_user.check_password("wrongpass"))
    
    def test_user_authentication_nonexistent_user(self):
        """Test that nonexistent user returns None"""
        found_user = User.query.filter_by(username="nonexistent").first()
        self.assertIsNone(found_user)
    
    def test_authentication_different_user_types(self):
        """Test that all user types can be found"""
        student = create_user("student1", "pass123", "student")
        employer = create_user("employer1", "pass123", "employer")
        staff = create_user("staff1", "pass123", "staff")
        
        found_student = User.query.filter_by(username="student1").first()
        found_employer = User.query.filter_by(username="employer1").first()
        found_staff = User.query.filter_by(username="staff1").first()
        
        self.assertIsNotNone(found_student)
        self.assertIsNotNone(found_employer)
        self.assertIsNotNone(found_staff)
        
        self.assertEqual(found_student.role, "student")
        self.assertEqual(found_employer.role, "employer")
        self.assertEqual(found_staff.role, "staff")
