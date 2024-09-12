from flask import Flask, jsonify, request
from model import Admin, Instructor, db
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': "404 Not Found",
        'message': "The requested URL was not found on the server"
    }), 404

@app.route('/login',methods=["POST"])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.password == password:
        access_token = create_access_token(identity = {'username': admin.username})
        return {'message': access_token}, 200
        
    print("Invalid credentials")
    return {'message': 'Invalid credentials'}, 401

@app.route('/instructors',methods=["GET"])
# @jwt_required()
def get_instructors():
    instructors = Instructor.query.all()
    return jsonify([instructor.to_dict() for instructor in instructors])

@app.route('/instructor/<int:id>')
# @jwt_required()
def get_user(id):
    instructor = Instructor.query.get_or_404(id)
    return jsonify(instructor.to_dict())

@app.route('/instructors', methods=['POST'])
# @jwt_required()
def add_instructors():
    data = request.form
    print(request.files)
    file = request.files['photo']
    print(data)
    new_instructor = Instructor(name=data['name'], linkedin=data['linkedin'], email=data['email'], bio=data['bio'], photo=file.read(), courses=data['courses'], category=data['category'])

    try:
        db.session.add(new_instructor)
        db.session.commit()
        return {'message': 'Instructor Added Successfully'}, 201
    except IntegrityError:
        db.session.rollback()
        if Instructor.query.filter_by(linkedin=data['linkedin']).first():
            return {'message': 'LinkedIn profile already exists.'}, 400
        if Instructor.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists.'}, 400
        return {'message': 'An error occurred while adding the instructor.'}, 400

@app.route('/instructor/<int:id>', methods=['PUT'])
# @jwt_required()
def update_instructor(id):
    data = request.form
    print(type(data))
    print(data)
    instructor = Instructor.query.get_or_404(id)
    instructor.name = data['name']
    instructor.linkedin=data['linkedin']
    instructor.email = data['email']
    instructor.bio=data['bio']
    
    if 'photo' in request.files:
        file = request.files['photo']
        instructor.photo=file.read()
    else:
        print("Photo not changed")

    instructor.courses=data['courses']
    instructor.category=data['category']

    try:
        db.session.commit()
        return {'message': 'Instructor updated Successfully'}, 200
    except IntegrityError:
        db.session.rollback()
        if Instructor.query.filter(Instructor.id != id, Instructor.linkedin == data['linkedin']).first():
            return {'message': 'LinkedIn profile already exists.'}, 400
        if Instructor.query.filter(Instructor.id != id, Instructor.email == data['email']).first():
            return {'message': 'Email already exists.'}, 400
        return {'message': 'An error occurred while updating the instructor.'}, 400
    
@app.route('/instructor/<int:id>', methods=['DELETE'])
# @jwt_required()
def delete_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



    