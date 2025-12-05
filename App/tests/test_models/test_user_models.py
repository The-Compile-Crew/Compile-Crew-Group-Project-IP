import unittest
from werkzeug.security import check_password_hash
from App.models import User, Student, Employer, Staff
from App.database import db
from App.main import create_app


class UserModelUnitTests(unittest.TestCase):
    
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
    
    def test_create_user(self):
        user = User("testuser", "testpass", "student")
        self.assertEqual(user.username, "testuser")
        self.assertNotEqual(user.password, "testpass")  # Password should be hashed
        self.assertEqual(user.role, "student")
    
    def test_check_password(self):
        user = User("testuser", "testpass", "employer")
        self.assertTrue(user.check_password("testpass"))
        self.assertFalse(user.check_password("wrongpass"))
    
    def test_password_hashing(self):
        raw_password = "securepass"
        user = User("alice", raw_password, "staff")
        self.assertTrue(check_password_hash(user.password, raw_password))
    
    def test_create_student(self):
        # Create user first
        user = User("john_student", "studentpass", "student")
        db.session.add(user)
        db.session.flush()
        
        student = Student("john_student", user.id, student_id="816999999")
        self.assertEqual(student.username, "john_student")
        # Student model doesn't have role attribute, uses user.role
    
    def test_create_employer(self):
        employer = Employer("alice_employer", "employerpass")
        self.assertEqual(employer.username, "alice_employer")
        # Employer model doesn't have role attribute, uses user.role
    
    def test_create_staff(self):
        staff = Staff("bob_staff", "staffpass")
        self.assertEqual(staff.username, "bob_staff")
        # Staff model doesn't have role attribute, uses user.role
