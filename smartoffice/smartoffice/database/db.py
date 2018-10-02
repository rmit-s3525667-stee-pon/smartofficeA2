"""This module create and run database for the system"""


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

USER = 'root'
PASS = 'password'
HOST = '35.201.22.140'
DBNAME = 'smartoffice-db'

# Open connection to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Patient database model
class Patient(db.Model):
    """Initialise Patient model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(80), unique=True)
    birthday = db.Column(db.Date, unique=False)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self, name, phone, birthday, email):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('name','phone','birthday','email')  

patient_schema = PatientSchema()
patients_schema = PatientSchema(many = True)

# Doctor database model
class Doctor(db.Model):
    """Initialise Doctor model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    major = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, major, email):
        self.name = name
        self.major = major
        self.email = email

class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('name','major','email')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many = True)

# Clerk database model
class Clerk(db.Model):
    """Initialise Clerk model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class ClerkSchema(ma.Schema):
    class Meta:
        fields = ('name','email')

clerk_schema = ClerkSchema()
clerks_schema = ClerkSchema(many = True)

# Appointment database model
class Appointment(db.Model):
    """Initialise Appointment model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique=False)
    date = db.Column(db.Date, unique=False)
    time_start = db.Column(db.Time, unique=False)
    time_end = db.Column(db.Time, unique=False)
    patient_id = db.Column(db.Integer, unique=False)
    event_id = db.Column(db.String(120), unique=False)

    def __init__(self, doctor_id, date, time_start, time_end, patient_id, event_id):
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.patient_id = patient_id
        self.event_id = event_id

class AppointmentSchema(ma.Schema):
    class Meta:
        fields = ('doctor_id','date','time_start','time_end', 'patient_id', 'event_id')

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many = True)

# Medical Record database model
class MedicalRecord(db.Model):
    """Initialise Medical Record model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique = False)
    patient_id = db.Column(db.Integer, unique = False)
    appointment_id = db.Column(db.Integer, unique = False)
    notes = db.Column(db.String(3000), unique = False)

    def __init__(self, doctor_id, patient_id, appointment_id, notes):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.notes = notes

class MedicalRecordSchema(ma.Schema):
    class Meta:
        fields = ('doctor_id','patient_id','appointment_id', 'notes')

medical_report_schema = AppointmentSchema()
medical_reports_schema = AppointmentSchema(many = True)

# Availability database model
class Availability(db.Model):
    """Initialise Availability model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique=False)
    date = db.Column(db.Date, unique=False)
    time_start = db.Column(db.Time, unique=False)
    time_end = db.Column(db.Time, unique=False)
    event_id = db.Column(db.String(120), unique=False)

    def __init__(self, doctor_id, date, time_start, time_end, event_id):
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.event_id = event_id

class AvailabilitySchema(ma.Schema):
    class Meta:
        fields = ('doctor_id','date','time_start','time_end', 'event_id')

availability_schema = AvailabilitySchema()
availability_schema = AvailabilitySchema(many = True)


