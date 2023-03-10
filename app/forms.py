from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import EqualTo, InputRequired

class SignUpForm(FlaskForm):
    firstname = StringField("First Name", validators = [InputRequired()])
    lastname = StringField("Last Name", validators = [InputRequired()])
    email = EmailField("Email", validators = [InputRequired()])
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators =[InputRequired()])
    confirmpass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators =[InputRequired()])
    submit = SubmitField()

class AddressForm(FlaskForm):
    firstname = StringField("First Name", validators = [InputRequired()])
    lastname = StringField("Last Name", validators = [InputRequired()])
    phone_number = StringField('Phone Number', validators = [InputRequired()])
    address = StringField('Address', validators = [InputRequired()])
    submit = SubmitField()