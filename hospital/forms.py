from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from hospital.models import *

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=1, max=10)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=150)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=7, max=15)])
    username = StringField('Username',
                           validators=[DataRequired(),
                            Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken ')

class LoginForm(FlaskForm): 
    username = StringField('Username',
                           validators=[DataRequired(),
                            Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddDoctorForm(FlaskForm):
    department_id = IntegerField('Department ID', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username',
                           validators=[DataRequired(),
                            Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(min=2, max=100)])
    experience = IntegerField('Years of Experience', validators=[DataRequired()])
    pph = IntegerField('Patients Per Hour', validators=[DataRequired()])
    # department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Doctor')
    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken ')
        
# class BookAppointmentForm(FlaskForm):
#     department = Select
    