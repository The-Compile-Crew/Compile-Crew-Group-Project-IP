import unittest
from App.models import User, Student, Employer, Staff
from App.controllers import create_user
from App.database import db
from App.main import create_app


class UserControllerUnitTests(unittest.TestCase):
    
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
    
    def test_create_student(self):
        user = create_user("john_student", "password123", "student", student_id="816000001")
        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "john_student")
        self.assertEqual(user.role, "student")
        # Verify Student record was created
        student = Student.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(student)
    
    def test_create_employer(self):
        user = create_user("alice_employer", "password456", "employer")
        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "alice_employer")
        self.assertEqual(user.role, "employer")
        # Verify Employer record was created
        employer = Employer.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(employer)
    
    def test_create_staff(self):
        user = create_user("bob_staff", "password789", "staff")
        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "bob_staff")
        self.assertEqual(user.role, "staff")
        # Verify Staff record was created
        staff = Staff.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(staff)
    
    def test_create_user_with_duplicate_username(self):
        """Test that duplicate usernames are handled"""
        user1 = create_user("duplicate_user", "password123", "student", student_id="816000099")
        self.assertIsNotNone(user1)
        
        # Attempting to create another user with same username should be handled
        user2 = create_user("duplicate_user", "password456", "employer")
        # Should return False on duplicate
        self.assertFalse(user2)
