import unittest
from App.models import Position, PositionStatus
from App.database import db


class PositionModelUnitTests(unittest.TestCase):
    
    def test_create_position(self):
        position = Position("Software Developer", 1, 5, "Develop software applications")
        self.assertEqual(position.title, "Software Developer")
        self.assertEqual(position.employer_id, 1)
        self.assertEqual(position.number_of_positions, 5)
        self.assertEqual(position.description, "Develop software applications")
        self.assertEqual(position.status, PositionStatus.open)
    
    def test_position_default_status(self):
        position = Position("Data Analyst", 2, 3)
        self.assertEqual(position.status, PositionStatus.open)
    
    def test_position_with_filled_count(self):
        position = Position("UX Designer", 3, 2)
        position.filled = 1
        self.assertEqual(position.filled, 1)
        self.assertEqual(position.number_of_positions, 2)
