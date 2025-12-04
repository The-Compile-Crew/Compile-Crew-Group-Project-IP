import unittest
from App.models import Position, Employer, PositionStatus
from App.controllers import create_user, open_position, get_positions_by_employer
from App.database import db
from App.main import create_app


class PositionControllerUnitTests(unittest.TestCase):
    
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
    
    def test_create_position(self):
        user = create_user("employer1", "pass", "employer")
        position = open_position(user.id, "Software Dev", 5)
        self.assertIsNotNone(position)
        self.assertEqual(position.title, "Software Dev")
        self.assertEqual(position.number_of_positions, 5)
    
    def test_create_position_invalid_employer(self):
        # Try to create position with non-existent employer
        position = open_position(9999, "Invalid Position", 1)
        self.assertIsNone(position)
    
    def test_get_positions_by_employer(self):
        user = create_user("employer2", "pass", "employer")
        open_position(user.id, "Position 1", 2)
        open_position(user.id, "Position 2", 3)
        
        positions = get_positions_by_employer(user.id)
        self.assertEqual(len(positions), 2)
    
    def test_position_capacity(self):
        user = create_user("employer3", "pass", "employer")
        position = open_position(user.id, "Internship", 10)
        self.assertEqual(position.number_of_positions, 10)
