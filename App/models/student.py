from App.database import db
from App.models.user import User
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    student_id = db.Column(db.String(32), nullable=False, unique=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(256))
    degree = db.Column(db.String(256))
    phone = db.Column(db.String(256))
    gpa = db.Column(db.Float)
    resume = db.Column(db.String(256))

    def __init__(self, username, user_id, student_id):
        self.username = username
        self.user_id = user_id
        self.student_id = student_id

