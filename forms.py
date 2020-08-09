import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import validators,StringField,PasswordField,StringField,SubmitField
from database import db,cursor

class signupForm(FlaskForm):
    user_name = StringField('UserName',validators=[validators.DataRequired(),validators.Length(min=3,max=20)])
    email     = StringField('Email',validators=[validators.DataRequired(),validators.Email()])
    photo     = FileField('Picture',validators=[FileRequired(),FileAllowed(['jpg','png'],message='Images Only')])
    password  = PasswordField('Password',validators=[validators.DataRequired()])
    submit    = SubmitField('SignUp')
    def validate_email(self,feild):
        cursor.execute('SELECT * FROM users WHERE email=%s',(feild.data,))
        if cursor.fetchone():
            raise validators.ValidationError("User Exists")
    def validate_password(self,field):
        regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
        if not regex.search(field.data):
            raise validators.ValidationError('Requirement Not Met')

class loginForm(FlaskForm):
    email = StringField('Email',validators=[validators.DataRequired(),validators.Email()])
    password = PasswordField('Password',validators=[validators.DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self,field):
        cursor.execute('SELECT * FROM users WHERE email=%s',(field.data,))
        user = cursor.fetchone()
        if not (user and user[3] == field.data):
            raise validators.ValidationError("Invalid Email")
