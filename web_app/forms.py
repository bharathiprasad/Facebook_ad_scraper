from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms import validators, ValidationError

class SignupForm(Form):
    username = TextField('Username', [validators.Required("Enter your username")])
    password = PasswordField('Password', [validators.Required('Enter your password')])
    retype_password = PasswordField('Retype Password', [validators.Required('Enter your password again')])
    submit = SubmitField('Signup')

class LoginForm(Form):
    username = TextField('Username', [validators.Required("Enter your username")])
    password = PasswordField('Password', [validators.Required('Enter your password')])
    submit = SubmitField('Login')
