from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Student, Result, Course

app = Flask(__name__)

# configure db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.sqlite'
app.config['SQLALCHEMY_ECHO'] = True

# setup migration tool
migrate = Migrate(app, db, render_as_batch=True)

# link our app with the db
db.init_app(app)

# base/index/root route
@app.route('/')
def hello_world():
    return "Hello, World"

@app.get('/students')
def students():
    students = Student.query.all()
    results = []

    for student in students:
        results.append(student.to_dict())

    return results

@app.get('/students/<int:student_id>')
def student(student_id):
    student = Student.query.filter_by(id=student_id).first()

    if student == None:
        return make_response({"message": "Student not found"}, 404)

    return student.to_dict()

@app.get('/results')
def results():
    results = []

    for result in Result.query.all():
        results.append(result.to_dict())

    return results

@app.get('/courses/<int:course_id>')
def course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    if course == None:
        return make_response({"message": "Course not found", "error": True}, 404)

    return make_response({"error": False, "data": course.to_dict()}, 200)

@app.get('/courses/<int:course_id>/students')
def course_students(course_id):
    course = Course.query.filter_by(id=course_id).first()

    if course == None:
        return make_response({"message": "Course not found", "error": True}, 404)

    students = []

    for student in course.students:
        students.append(student.to_dict(rules=('-results',)))

    return make_response({"error": False, "data": students}, 200)

@app.post('/students')
def create_user():
    student = Student(first_name="Brian", last_name="Njuguna",
                      email="brian@gmail.com", phone="0712345678", age=22)

    # adds the student instance to the transaction
    db.session.add(student)

    # commits the transaction
    db.session.commit()

    return "User created"
