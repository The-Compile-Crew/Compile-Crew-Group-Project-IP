from App.database import db
from App.models.user import User
from sqlalchemy import Enum
import enum  


class DecisionStatus(enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    accepted = "accepted"
    rejected = "rejected"
    #removed pending status as it is not needed in the state pattern

# Base class for states
class ShortlistState:
    def advance(self, context):
        raise NotImplementedError("advance() must be implemented by subclasses")

    def accept(self, context):
        raise NotImplementedError("accept() must be implemented by subclasses")

    def reject(self, context):
        raise NotImplementedError("reject() must be implemented by subclasses")

    def get_status(self):
        raise NotImplementedError("get_status() must be implemented by subclasses")

class Shortlist(db.Model):
    __tablename__ = 'shortlist'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    title = db.Column(db.String(512), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    status = db.Column(Enum(DecisionStatus, native_enum=False), nullable=False, default=DecisionStatus.applied)
    state = db.Column(db.String, nullable=True)
    student = db.relationship('Student', backref=db.backref('shortlist', lazy=True))
    position = db.relationship('Position', backref=db.backref('shortlist', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('shortlist', lazy=True))
    
     
    

    def __init__(self, student_id, position_id, staff_id, title, state):
        self.student_id = student_id
        self.position_id = position_id
        self.status = DecisionStatus.applied
        self.staff_id = staff_id
        self.title = title
        self.state = state
        self.set_state_from_status(self.status)

#new method to set state based on status
    def set_state(self, state: ShortlistState):
            self.state = state

    def get_state(self):
            return self.state

    def set_state_from_status(self, status: DecisionStatus):
        if status == DecisionStatus.applied:
            from App.models.shortliststate import AppliedState
            self.state = AppliedState()

        elif status == DecisionStatus.shortlisted:
            from App.models.shortliststate import ShortlistedState
            self.state = ShortlistedState()

        elif status == DecisionStatus.accepted:
            from App.models.shortliststate import AcceptedState
            self.state = AcceptedState()

        elif status == DecisionStatus.rejected:
            from App.models.shortliststate import RejectedState
            self.state = RejectedState()

    #removed update_status method
    def student_shortlist(self, student_id):
        return db.session.query(Shortlist).filter_by(student_id=student_id).all()

    def position_shortlist(self, position_id):
        return db.session.query(Shortlist).filter_by(position_id=position_id).all()
    
#methods per state class
    def advance(self):
        self.state.advance(self)
        db.session.commit()

    def accept(self):
        self.state.accept(self)
        db.session.commit()

    def reject(self):
        self.state.reject(self)
        db.session.commit()

    def get_status(self):
        return self.state.get_status()
        
    def toJSON(self):
        return{
            "id": self.id,
            "title": self.title,
            "student_id": self.student_id,
            "position_id": self.position_id,
            "staff_id": self.staff_id,
            "status": self.status.value
        }
    
      