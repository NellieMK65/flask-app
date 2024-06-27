from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Student, Result

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


@app.route('/about')
def about():
    return "Learning the basics of flask"

@app.route('/contact')
def contact():
    return "Contact"

@app.route('/courses', methods=['POST'])
def create_course():
    return "Course created"

@app.route('/courses', methods=['GET'])
def courses():
    # courses = Course.find_all(query)

    return "Return a list of courses"

@app.route('/courses/<int:course_id>', methods=['PATCH', 'PUT'])
def update_course(course_id):
    return f"Updating course {course_id}"

@app.route('/courses/<int:course_id>', methods=['GET'])
def course(course_id):
    # course = Course.find_one(course_id)

    return f"Accessing course {course_id}"

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    return f"Deleting course {course_id}"

@app.get('/students')
def students():
    students = Student.query.all()
    results = []

    for student in students:
        results.append(student.to_dict())

    return results

@app.get('/students/<int:student_id>')
def student(student_id):
    student = Student.query.filter_by(id = student_id).first()

    if student == None:
        return make_response({ "message": "Student not found" }, 404)

    return student.to_dict()

@app.get('/results')
def results():
    results = []

    for result in Result.query.all():
        results.append(result.to_dict())

    return results

@app.post('/students')
def create_user():
    student = Student(first_name = "Brian", last_name = "Njuguna", email="brian@gmail.com", phone="0712345678", age=22)

    # adds the student instance to the transaction
    db.session.add(student)

    # commits the transaction
    db.session.commit()

    return "User created"

class Course:

    @classmethod
    def find_one(id):
        # retrieve using id
        # SELECT * FROM courses WHERE id = ?
        return None

    @classmethod
    def find_all(query):

        # SELECT * FROM courses ORDER BY created_at ?
        return []
