import unittest
from werkzeug.security import check_password_hash
from App.models import User, Student, Employer, Staff


class UserModelUnitTests(unittest.TestCase):
    
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
        student = Student("john_student", "studentpass")
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
