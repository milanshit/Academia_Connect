import base64
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    linkedin = db.Column(db.String(200), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    bio = db.Column(db.Text ,nullable = True)
    photo = db.Column(db.LargeBinary, unique = True)
    courses = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(100), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "linkedin": self.linkedin,
            "email": self.email,
            "bio": self.bio,
            'photo': base64.b64encode(self.photo).decode('utf-8'),
            "courses": self.courses,
            "category": self.category
        }
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)