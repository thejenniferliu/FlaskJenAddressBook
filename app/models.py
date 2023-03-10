from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    address = db.relationship('Address', backref = 'author')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

    def to_dict(self):
        return{
            'id': self.id,
            'first name': self.firstname,
            'last name': self.lastname,
            'email': self.email,
            'username': self.username,
            'password': self.password
        }

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.id} | {self.address}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'firstname', 'lastname', 'address', 'phone_number'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()