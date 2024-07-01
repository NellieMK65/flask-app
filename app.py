from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource, Api

from models import db
from resources.student import StudentResource
from resources.course import CourseResource, CourseStudentsResource

app = Flask(__name__)
api = Api(app)
# configure db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.sqlite'
app.config['SQLALCHEMY_ECHO'] = True

# setup migration tool
migrate = Migrate(app, db, render_as_batch=True)

# link our app with the db
db.init_app(app)
class HelloWorld(Resource):
    def get(self):
        return { "message": "Hello world" }

api.add_resource(HelloWorld, '/')
api.add_resource(StudentResource, '/students', '/students/<int:id>')
api.add_resource(CourseResource, '/courses', '/courses/<int:id>')
api.add_resource(CourseStudentsResource, '/courses/<int:course_id>/students')
