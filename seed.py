from app import app
from models import db, Student

with app.app_context():
    print("Start seeding...")

    new_students = []

    new_students.append(Student(first_name="Joseph", last_name="Mburu", email="joseph@gmail.com",phone="0712345677", age=19))
    new_students.append(Student(first_name="Cindy", last_name="Mutisya", email="cindy@gmail.com", phone="0712345679", age=20))

    db.session.add_all(new_students)
    db.session.commit()

    print("Database seeded")
