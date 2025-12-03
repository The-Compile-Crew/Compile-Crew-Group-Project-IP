from sqlalchemy import false
from App.models import Shortlist, Position, Staff, Student
from App.database import db

def add_student_to_shortlist(student_id, position_id, staff_id, student_name, student_identifier, details):
    teacher = db.session.query(Staff).filter_by(user_id=staff_id).first()
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    if student is None or teacher is None:
        return False
    list = db.session.query(Shortlist).filter_by(student_id=student.id, position_id=position_id).first()
    position = db.session.query(Position).filter(
        Position.id == position_id,
        Position.number_of_positions > 0,
        Position.status == "open"
    ).first()
    if teacher and not list and position:
        from App.models.shortlist import DecisionStatus
        shortlist = Shortlist(
            student_id=student.id,
            position_id=position.id,
            staff_id=teacher.id,
            title=position.title,
            state=None,
            student_name=student_name,
            student_identifier=student_identifier,
            details=details
        )
        shortlist.status = DecisionStatus.shortlisted
        db.session.add(shortlist)
        db.session.commit()
        return shortlist
    return False

def decide_shortlist(student_id, position_id, decision):
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    shortlist = db.session.query(Shortlist).filter_by(student_id=student.id, position_id=position_id).first()
    position = db.session.query(Position).filter(Position.id==position_id, Position.number_of_positions > 0).first()
    if shortlist and position:
        # Only allow decision if not already accepted/rejected
        if shortlist.status.value not in ["accepted", "rejected"]:
            if decision == "accepted":
                shortlist.status = "accepted"
            elif decision == "rejected":
                shortlist.status = "rejected"
            db.session.commit()
            position.update_number_of_positions(position.number_of_positions - 1)
        return shortlist
    return False


def get_shortlist_by_student(student_id):
    student = db.session.query(Student).filter_by(user_id=student_id).first()
    return db.session.query(Shortlist).filter_by(student_id=student.id).all()

def get_shortlist_by_position(position_id):
    return db.session.query(Shortlist).filter_by(position_id=position_id).all()
