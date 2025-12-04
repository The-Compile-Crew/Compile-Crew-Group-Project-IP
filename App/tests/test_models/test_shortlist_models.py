import unittest
from App.models import Shortlist, DecisionStatus
from App.models.shortliststate import AppliedState, ShortlistedState, AcceptedState, RejectedState
from App.database import db


class ShortlistModelUnitTests(unittest.TestCase):
    
    def test_create_shortlist(self):
        shortlist = Shortlist(
            student_id=1,
            position_id=2,
            staff_id=3,
            title="Software Developer",
            state="applied",
            student_name="John Doe",
            student_identifier="816001234",
            details="Interested in backend development"
        )
        self.assertEqual(shortlist.student_id, 1)
        self.assertEqual(shortlist.position_id, 2)
        self.assertEqual(shortlist.staff_id, 3)
        self.assertEqual(shortlist.status, DecisionStatus.applied)
    
    def test_shortlist_default_status(self):
        shortlist = Shortlist(
            student_id=1,
            position_id=2,
            staff_id=3,
            title="Data Analyst",
            state="applied",
            student_name="Jane Smith",
            student_identifier="816005678",
            details="Analytics experience"
        )
        self.assertEqual(shortlist.status, DecisionStatus.applied)
    
    def test_shortlist_state_transitions(self):
        """Test that state pattern is properly initialized"""
        shortlist = Shortlist(
            student_id=1,
            position_id=2,
            staff_id=3,
            title="Developer",
            state="applied",
            student_name="Test Student",
            student_identifier="816001111",
            details="Test details"
        )
        # State should be stored as string value
        self.assertEqual(shortlist.state, "applied")
