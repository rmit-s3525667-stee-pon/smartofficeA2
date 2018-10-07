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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Patient(db.Model):
    """Doctor Class""" 
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
    """Patient Schema to format return data""" 
    class Meta:
        fields = ('id','name','phone','birthday','email')
    
patient_schema = PatientSchema()
patients_schema = PatientSchema(many = True)

class Doctor(db.Model):
    """Patient Class""" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    major = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)
    calendar_id = db.Column(db.String(120), unique=True)

    def __init__(self, name, major, email, calendar_id):
        self.name = name
        self.major = major
        self.email = email
        self.calendar_id = calendar_id

class DoctorSchema(ma.Schema):
    """Doctor Schema to format return data""" 
    class Meta:
        fields = ('id','name','major','email', 'calendar_id')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many = True)

class Clerk(db.Model):
    """Clerk Class""" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class ClerkSchema(ma.Schema):
    """Clerk Schema to format return data""" 
    class Meta:
        fields = ('id','name','email')

clerk_schema = ClerkSchema()
clerks_schema = ClerkSchema(many = True)

class Appointment(db.Model):
    """Appointment Class""" 
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique=False)
    date = db.Column(db.Date, unique=False)
    time_start = db.Column(db.Time, unique=False)
    time_end = db.Column(db.Time, unique=False)
    patient_id = db.Column(db.Integer, unique=False)
    event_id = db.Column(db.String, unique=False)

    def __init__(self, doctor_id, date, time_start, time_end, patient_id, event_id):
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.patient_id = patient_id
        self.event_id = event_id

class AppointmentSchema(ma.Schema):
    """Appointent Schema to format return data""" 
    class Meta:
        fields = ('id','doctor_id','date','time_start','time_end', 'patient_id', 'event_id')

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many = True)

class MedicalRecord(db.Model):
    """Medical Record Class""" 
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique = False)
    patient_id = db.Column(db.Integer, unique = False)
    date = db.Column(db.Date, unique=False)
    notes = db.Column(db.String(3000), unique = False)

    def __init__(self, doctor_id, patient_id, date, notes):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.date = date
        self.notes = notes

class MedicalRecordSchema(ma.Schema):
    """Medical Record Schema to format return data""" 
    class Meta:
        fields = ('id','doctor_id','patient_id','date', 'notes')

medical_record_schema = MedicalRecordSchema()
medical_records_schema = MedicalRecordSchema(many = True)

class Availability(db.Model):
    """Availability Class""" 
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
    """Availability Schema to format return data""" 
    class Meta:
        fields = ('id','doctor_id','date' ,'time_start','time_end', 'event_id')

availability_schema = AvailabilitySchema()
availabilities_schema = AvailabilitySchema(many = True)


