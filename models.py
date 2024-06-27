from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

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
class Student(db.Model, SerializerMixin):
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
    """
    When implementing a one to one rltship we need to add
    uselist=False option.
    """
    # result = db.relationship('Result', uselist=False)

    serialize_rules = ('-results.student',)

class Result(db.Model, SerializerMixin):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    # course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    student = db.relationship('Student', back_populates="results")

    # prevent student from loading results
    serialize_rules = ('-student.results',)
    # select specific fields
    serialize_only = ('id', 'marks', 'student')
