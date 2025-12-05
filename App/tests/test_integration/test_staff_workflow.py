import unittest
from App.main import create_app
from App.database import db
from App.controllers import (
    create_user,
    open_position,
    add_student_to_shortlist,
    decide_shortlist,
    get_shortlist_by_student,
    get_shortlist_by_position
)
from App.models import Shortlist, Position, Student, DecisionStatus, PositionStatus


class StaffWorkflowIntegrationTests(unittest.TestCase):
    """Integration tests for complete staff workflows"""
    
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
    
    def test_complete_shortlist_workflow(self):
        """Test complete workflow: staff adds student, employer decides"""
        # Create all users
        staff_user = create_user("staff_workflow", "pass", "staff")
        student_user = create_user("student_workflow", "pass", "student", student_id="816000020")
        employer_user = create_user("employer_workflow", "pass", "employer")
        
        # Employer creates position
        position = open_position(employer_user.id, "Full Stack Dev", 3)
        self.assertIsNotNone(position)
        self.assertEqual(position.status, PositionStatus.open)
        
        # Staff adds student to shortlist
        shortlist = add_student_to_shortlist(
            student_user.id,
            position.id,
            staff_user.id,
            "Workflow Student",
            "816000020",
            "Perfect fit for the role"
        )
        self.assertIsNotNone(shortlist)
        self.assertEqual(shortlist.status, DecisionStatus.shortlisted)
        
        # Employer reviews and accepts
        result = decide_shortlist(student_user.id, position.id, "accepted")
        self.assertIsNotNone(result)
        self.assertEqual(result.status.value, "accepted")
        
        # Verify position capacity decreased
        db.session.refresh(position)
        self.assertEqual(position.number_of_positions, 2)
    
    def test_multiple_students_one_position(self):
        """Test staff adding multiple students to one position"""
        staff_user = create_user("staff_multi", "pass", "staff")
        employer_user = create_user("employer_multi", "pass", "employer")
        
        # Create students
        student1 = create_user("student_m1", "pass", "student", student_id="816000021")
        student2 = create_user("student_m2", "pass", "student", student_id="816000022")
        student3 = create_user("student_m3", "pass", "student", student_id="816000023")
        
        # Create position
        position = open_position(employer_user.id, "Data Science", 5)
        
        # Staff adds all students
        s1 = add_student_to_shortlist(student1.id, position.id, staff_user.id, "Student 1", "816000021", "Good")
        s2 = add_student_to_shortlist(student2.id, position.id, staff_user.id, "Student 2", "816000022", "Better")
        s3 = add_student_to_shortlist(student3.id, position.id, staff_user.id, "Student 3", "816000023", "Best")
        
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)
        self.assertIsNotNone(s3)
        
        # Verify all in position's shortlist
        shortlists = get_shortlist_by_position(position.id)
        self.assertEqual(len(shortlists), 3)
    
    def test_one_student_multiple_positions(self):
        """Test staff adding one student to multiple positions"""
        staff_user = create_user("staff_positions", "pass", "staff")
        student_user = create_user("student_positions", "pass", "student", student_id="816000024")
        employer_user = create_user("employer_positions", "pass", "employer")
        
        # Create positions
        pos1 = open_position(employer_user.id, "Frontend", 2)
        pos2 = open_position(employer_user.id, "Backend", 2)
        pos3 = open_position(employer_user.id, "Full Stack", 2)
        
        # Add student to all positions
        s1 = add_student_to_shortlist(student_user.id, pos1.id, staff_user.id, "Versatile Student", "816000024", "Frontend skills")
        s2 = add_student_to_shortlist(student_user.id, pos2.id, staff_user.id, "Versatile Student", "816000024", "Backend skills")
        s3 = add_student_to_shortlist(student_user.id, pos3.id, staff_user.id, "Versatile Student", "816000024", "Full stack skills")
        
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)
        self.assertIsNotNone(s3)
        
        # Verify all in student's shortlist
        shortlists = get_shortlist_by_student(student_user.id)
        self.assertEqual(len(shortlists), 3)
    
    def test_shortlist_capacity_limit(self):
        """Test that decisions properly update position capacity"""
        staff_user = create_user("staff_capacity", "pass", "staff")
        employer_user = create_user("employer_capacity", "pass", "employer")
        
        # Create position with limited capacity
        position = open_position(employer_user.id, "Limited Role", 2)
        
        # Create students
        student1 = create_user("s_cap1", "pass", "student", student_id="816000025")
        student2 = create_user("s_cap2", "pass", "student", student_id="816000026")
        student3 = create_user("s_cap3", "pass", "student", student_id="816000027")
        
        # Add all to shortlist
        add_student_to_shortlist(student1.id, position.id, staff_user.id, "Cap1", "816000025", "A")
        add_student_to_shortlist(student2.id, position.id, staff_user.id, "Cap2", "816000026", "B")
        add_student_to_shortlist(student3.id, position.id, staff_user.id, "Cap3", "816000027", "C")
        
        # Accept first two
        decide_shortlist(student1.id, position.id, "accepted")
        decide_shortlist(student2.id, position.id, "accepted")
        
        # Check capacity
        db.session.refresh(position)
        self.assertEqual(position.number_of_positions, 0)
    
    def test_rejection_decreases_capacity(self):
        """Test that rejecting also decreases position capacity"""
        staff_user = create_user("staff_reject", "pass", "staff")
        student_user = create_user("student_reject", "pass", "student", student_id="816000028")
        employer_user = create_user("employer_reject", "pass", "employer")
        
        position = open_position(employer_user.id, "Reject Test", 5)
        original = position.number_of_positions
        
        add_student_to_shortlist(student_user.id, position.id, staff_user.id, "Reject Student", "816000028", "Details")
        
        # Reject the application
        decide_shortlist(student_user.id, position.id, "rejected")
        
        db.session.refresh(position)
        self.assertEqual(position.number_of_positions, original - 1)
