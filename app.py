import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS

from models import db
from resources.student import StudentResource
from resources.course import CourseResource, CourseStudentsResource

app = Flask(__name__)
api = Api(app)
# configure db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = True

# setup cors
CORS(app)

# setup migration tool
migrate = Migrate(app, db, render_as_batch=True)

# link our app with the db
db.init_app(app)
class HelloWorld(Resource):
    def get(self):
        return { "message": "Hello world" }

api.add_resource(HelloWorld, '/')
# PATCH -> /students/1
# DELETE -> /students/1
# GET one -> /student/1
api.add_resource(StudentResource, '/students', '/students/<int:id>')
api.add_resource(CourseResource, '/courses', '/courses/<int:id>')
api.add_resource(CourseStudentsResource, '/courses/<int:course_id>/students')
