from hospital import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password_hash= db.Column(db.String(120),nullable=False)
    role = db.Column(db.String(20),nullable=False)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    department_id = db.Column(db.Integer,db.ForeignKey('departments.id'),nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    specialization = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text,nullable=True)
    pph = db.Column(db.Integer,nullable=False)  # per patient hour
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    appointments = db.relationship('Appointment',backref='doctor',lazy=True)

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer,primary_key=True,)
    name = db.Column(db.String(100),nullable=False,unique=True)
    doctors = db.relationship('Doctor',backref='department',lazy=True)
    
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    age = db.Column(db.Integer,nullable=True)
    gender = db.Column(db.String(10),nullable=True)
    address = db.Column(db.String(150),nullable=True)
    contact_number = db.Column(db.String(15),nullable=True)
    appointments = db.relationship('Appointment',backref='patient',lazy=True)
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer,primary_key=True)
    dept_id = db.Column(db.Integer,db.ForeignKey('departments.id'),nullable=False)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctors.id'),nullable=False) 
    patient_id = db.Column(db.Integer,db.ForeignKey('patients.id'),nullable=False)
    appointment_date = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(20),default='Booked')
    treatment = db.relationship("Treatment",backref="appointment",uselist=False)
    department = db.relationship('Department', backref='dept_appointments', lazy=True)
    time_slot = db.Column(db.String(50), nullable=False)  # e.g., "08:00 - 12:00 am"
    date = db.Column(db.Date, nullable=False)
class Treatment(db.Model):
    __tablename__ = 'treatments'
    id = db.Column(db.Integer,primary_key=True)
    appointment_id = db.Column(db.Integer,db.ForeignKey('appointments.id'),nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text,nullable=False)
    prescription = db.Column(db.Text)

class Availability(db.Model):
    __tablename__ = 'availabilities'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)  # e.g., "2024-07-01 10:00-11:00"
    date = db.Column(db.Date, nullable=False)