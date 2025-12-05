import unittest
from App.models import Shortlist, Position, Student, Employer, Staff, DecisionStatus
from App.controllers import (
    create_user,
    open_position,
    add_student_to_shortlist,
    decide_shortlist,
    get_shortlist_by_student,
    get_shortlist_by_position
)
from App.database import db
from App.main import create_app


class ShortlistControllerUnitTests(unittest.TestCase):
    
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
    
    def test_add_student_to_shortlist(self):
        # Create users
        staff_user = create_user("staff1", "pass", "staff")
        student_user = create_user("student1", "pass", "student", student_id="816000001")
        employer_user = create_user("employer1", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "Software Dev", 5)
        
        # Get the actual student and staff records
        student = Student.query.filter_by(user_id=student_user.id).first()
        staff = Staff.query.filter_by(user_id=staff_user.id).first()
        
        # Add student to shortlist
        shortlist = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "John Doe",
            "816000001",
            "Great candidate"
        )
        
        self.assertIsNotNone(shortlist)
        self.assertEqual(shortlist.student_id, student.id)
        self.assertEqual(shortlist.position_id, position.id)
        self.assertEqual(shortlist.staff_id, staff.id)
        self.assertEqual(shortlist.status, DecisionStatus.shortlisted)
    
    def test_add_duplicate_shortlist_entry(self):
        # Create users
        staff_user = create_user("staff2", "pass", "staff")
        student_user = create_user("student2", "pass", "student", student_id="816000002")
        employer_user = create_user("employer2", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "Backend Dev", 3)
        
        # Add student to shortlist first time
        shortlist1 = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "Jane Doe",
            "816000002",
            "Excellent skills"
        )
        
        # Try adding same student to same position again
        shortlist2 = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "Jane Doe",
            "816000002",
            "Another attempt"
        )
        
        self.assertIsNotNone(shortlist1)
        self.assertFalse(shortlist2)  # Should fail
    
    def test_add_to_shortlist_invalid_student(self):
        # Create users
        staff_user = create_user("staff3", "pass", "staff")
        employer_user = create_user("employer3", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "DevOps", 2)
        
        # Try adding non-existent student
        shortlist = add_student_to_shortlist(
            9999,  # Invalid student ID
            position.id,
            staff_user.id,
            "Nobody",
            "816999999",
            "Ghost student"
        )
        
        self.assertFalse(shortlist)
    
    def test_decide_shortlist_accept(self):
        # Create users
        staff_user = create_user("staff4", "pass", "staff")
        student_user = create_user("student4", "pass", "student", student_id="816000004")
        employer_user = create_user("employer4", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "Data Analyst", 5)
        original_capacity = position.number_of_positions
        
        # Add student to shortlist
        shortlist = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "Alice Smith",
            "816000004",
            "Strong analytical skills"
        )
        
        # Employer accepts the application
        result = decide_shortlist(student_user.id, position.id, "accepted")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.status.value, "accepted")
        # Position capacity should decrease
        db.session.refresh(position)
        self.assertEqual(position.number_of_positions, original_capacity - 1)
    
    def test_decide_shortlist_reject(self):
        # Create users
        staff_user = create_user("staff5", "pass", "staff")
        student_user = create_user("student5", "pass", "student", student_id="816000005")
        employer_user = create_user("employer5", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "UX Designer", 3)
        original_capacity = position.number_of_positions
        
        # Add student to shortlist
        shortlist = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "Bob Jones",
            "816000005",
            "Needs more experience"
        )
        
        # Employer rejects the application
        result = decide_shortlist(student_user.id, position.id, "rejected")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.status.value, "rejected")
        # Position capacity should decrease
        db.session.refresh(position)
        self.assertEqual(position.number_of_positions, original_capacity - 1)
    
    def test_get_shortlist_by_student(self):
        # Create users
        staff_user = create_user("staff6", "pass", "staff")
        student_user = create_user("student6", "pass", "student", student_id="816000006")
        employer_user = create_user("employer6", "pass", "employer")
        
        # Create multiple positions
        pos1 = open_position(employer_user.id, "Frontend Dev", 2)
        pos2 = open_position(employer_user.id, "Backend Dev", 2)
        
        # Add student to both positions
        add_student_to_shortlist(student_user.id, pos1.id, staff_user.id, "Test Student", "816000006", "Details 1")
        add_student_to_shortlist(student_user.id, pos2.id, staff_user.id, "Test Student", "816000006", "Details 2")
        
        # Get student's shortlist
        shortlists = get_shortlist_by_student(student_user.id)
        
        self.assertEqual(len(shortlists), 2)
    
    def test_get_shortlist_by_position(self):
        # Create users
        staff_user = create_user("staff7", "pass", "staff")
        student1 = create_user("student7a", "pass", "student", student_id="816000007")
        student2 = create_user("student7b", "pass", "student", student_id="816000008")
        employer_user = create_user("employer7", "pass", "employer")
        
        # Create position
        position = open_position(employer_user.id, "Intern", 5)
        
        # Add multiple students to position
        add_student_to_shortlist(student1.id, position.id, staff_user.id, "Student A", "816000007", "Detail A")
        add_student_to_shortlist(student2.id, position.id, staff_user.id, "Student B", "816000008", "Detail B")
        
        # Get position's shortlist
        shortlists = get_shortlist_by_position(position.id)
        
        self.assertEqual(len(shortlists), 2)
