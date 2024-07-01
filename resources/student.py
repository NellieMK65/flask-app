from flask_restful import Resource, reqparse
from models import db, Student

class StudentResource(Resource):
    # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True, help="First name is required")
    parser.add_argument('last_name', required=True, help="Last name is required")
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('phone', required=True, help="Phone number is required")
    parser.add_argument('age', type=int, required=True, help="Age is required")

    def get(self, id=None):
        if id == None:
            students = Student.query.all()
            results = []

            for student in students:
                results.append(student.to_dict())

            return results
        else:
            student = Student.query.filter_by(id=id).first()

            if student == None:
                return { "message": "Student not found" }, 404

            return student.to_dict()

    def post(self):
        data = StudentResource.parser.parse_args()

        # verify email and phone numbers are available
        email = Student.query.filter_by(email = data['email']).first()

        if email:
            return { "message": "Email already taken" }, 422

        phone = Student.query.filter_by(phone = data['phone']).first()

        if phone:
            return { "message": "Phone number already taken" }, 422

        student = Student(**data)

        # adds the student instance to the transaction
        db.session.add(student)

        # commits the transaction
        db.session.commit()

        return { "message": "Student created successfully" }
