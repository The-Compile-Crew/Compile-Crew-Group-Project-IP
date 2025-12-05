from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password, user_type, student_id=None):
    try:
        newuser = User(username=username, password=password, role=user_type)
        db.session.add(newuser)
        db.session.flush() 
        
        if user_type == "student":
            student = Student(username=username, user_id=newuser.id, student_id=student_id)
            db.session.add(student)
        elif user_type == "employer":
            employer = Employer(username=username, user_id=newuser.id)
            db.session.add(employer)
        elif user_type == "staff":
            staff = Staff(username=username, user_id=newuser.id)
            db.session.add(staff)
        else:
            print("Invalid user type")
            return False
        
        db.session.commit()
        return newuser
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users


def get_all_students_with_details():
    """Get all students with their username and student_id"""
    students = db.session.query(
        User.username,
        User.id.label('user_id'),
        Student.student_id,
        Student.id.label('student_table_id')
    ).join(Student, User.id == Student.user_id)
    students = students.filter(User.role == 'student').all()

    # Convert to list of dictionaries for easier template access
    student_list = []
    for student in students:
        student_list.append({
            'username': student.username,
            'student_id': student.student_id,
            'user_id': student.user_id
        })
    return student_list

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
