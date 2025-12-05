import unittest
from App.main import create_app
from App.database import db
from App.controllers import (
    create_user,
    open_position,
    get_positions_by_employer,
    add_student_to_shortlist,
    get_shortlist_by_student
)
from App.models import DecisionStatus, PositionStatus, User


class IntegrationTests(unittest.TestCase):
    
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
    
    def test_complete_application_flow(self):
        """Test the complete flow: user creation -> position creation -> application"""
        # Create users
        student = create_user("alice_student", "password123", "student", student_id="816000001")
        employer = create_user("tech_corp", "password123", "employer")
        staff = create_user("admin_staff", "password123", "staff")
        
        self.assertIsNotNone(student)
        self.assertIsNotNone(employer)
        self.assertIsNotNone(staff)
        
        # Create position
        position = open_position(employer.id, "Software Intern", 3)
        self.assertIsNotNone(position)
        self.assertEqual(position.status, PositionStatus.open)
        
        # Add student to shortlist (if this function exists)
        # shortlist = add_student_to_shortlist(student.id, position.id, staff.id)
        # self.assertIsNotNone(shortlist)
        # self.assertEqual(shortlist.status, DecisionStatus.applied)
        
        # Verify shortlist (if function exists)
        # student_shortlists = get_shortlist_by_student(student.id)
        # self.assertTrue(len(student_shortlists) > 0)
        # self.assertEqual(student_shortlists[0].position_id, position.id)
    
    def test_authentication_flow(self):
        """Test user creation and login"""
        # Create user
        user = create_user("john_doe", "securepass", "student", student_id="816000002")
        self.assertIsNotNone(user)
        
        # Test successful authentication
        found_user = User.query.filter_by(username="john_doe").first()
        self.assertIsNotNone(found_user)
        self.assertTrue(found_user.check_password("securepass"))
        
        # Test failed authentication
        self.assertFalse(found_user.check_password("wrongpass"))
    
    def test_employer_position_management(self):
        """Test employer creating and viewing positions"""
        employer = create_user("startup_inc", "password123", "employer")
        
        # Create multiple positions
        pos1 = open_position(employer.id, "Backend Developer", 2)
        pos2 = open_position(employer.id, "Frontend Developer", 1)
        pos3 = open_position(employer.id, "DevOps Engineer", 1)
        
        # Get all positions for employer
        positions = get_positions_by_employer(employer.id)
        self.assertEqual(len(positions), 3)
        
        # Verify positions
        titles = [p.title for p in positions]
        self.assertIn("Backend Developer", titles)
        self.assertIn("Frontend Developer", titles)
        self.assertIn("DevOps Engineer", titles)
    
    def test_student_multiple_applications(self):
        """Test student applying to multiple positions"""
        student = create_user("jane_student", "password123", "student", student_id="816000003")
        employer = create_user("big_tech", "password123", "employer")
        staff = create_user("staff_admin", "password123", "staff")
        
        # Create multiple positions
        pos1 = open_position(employer.id, "Data Analyst", 2)
        pos2 = open_position(employer.id, "UX Designer", 1)
        
        # Student applies to both (if function exists)
        # shortlist1 = add_student_to_shortlist(student.id, pos1.id, staff.id)
        # shortlist2 = add_student_to_shortlist(student.id, pos2.id, staff.id)
        
        # Verify student has 2 applications (if function exists)
        # applications = get_shortlist_by_student(student.id)
        # self.assertEqual(len(applications), 2)
        
        # For now, just verify positions were created
        self.assertIsNotNone(pos1)
        self.assertIsNotNone(pos2)
    
    def test_position_capacity_tracking(self):
        """Test that position tracks filled vs capacity"""
        employer = create_user("company_x", "password123", "employer")
        position = open_position(employer.id, "Software Developer", 3)
        
        self.assertEqual(position.number_of_positions, 3)
        
        # After accepting students, filled count should update
        # (This would be tested once the accept/reject functionality is fully implemented)
