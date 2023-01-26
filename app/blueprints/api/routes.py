from flask import request
from . import api
from app.models import User

@api.route('/')
def index():
    return 'this is not working and i dont know why'

@api.route('/users')
def get_users():
    users = User.query.all()
    return [u.to_dict() for u in users]

@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user.to_dict()

@api.route('/users', methods = ['POST'])
def create_user():
    if not request.is_json:
        return {'not it?'}, 400

    data = request.json

    for field in ['first name', 'last name', 'email', 'username', 'password']:
        if field not in data:
            return {'error'}, 400
    
    firstname = data.get('first name')
    lastname = data.get('last name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')


    new_user = User(firstname = firstname, lastname = lastname, email = email, username = username, password = password)
    return new_user.to_dict(), 201
