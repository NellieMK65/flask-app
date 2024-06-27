from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# initialize metadata
metadata = MetaData(naming_convention = convention)

db = SQLAlchemy(metadata = metadata)

# define models
class Student(db.Model):
    # define table
    __tablename__ = "students"

    # define columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Text, nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP)

    results = db.relationship('Result')

    def to_dict(self):

        converted_results = []

        for result in self.results:
            converted_results.append(result.to_dict())

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "results": converted_results
        }

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    # course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    student = db.relationship('Student', back_populates="results")

    def to_dict(self):
        return  {
            "id": self.id,
            "marks": self.marks,
        }
