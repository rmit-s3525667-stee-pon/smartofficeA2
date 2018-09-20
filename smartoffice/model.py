from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from smartoffice import db, ma

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('name','email')
    
patient_schema = PatientSchema()
patients_schema = PatientSchema(many = True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    major = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=False)

    def __init__(self, name, major, email):
        self.name = name
        self.major = major
        self.email = email

class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('name','major','email')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many = True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique=False)
    date = db.Column(db.Date, unique=False)
    time_start = db.Column(db.Time, unique=False)
    time_end = db.Column(db.Time, unique=False)
    patient_id = db.Column(db.Integer, unique=False)

    def __init__(self, doctor_id, date, time_start, time_end, patient_id):
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.patient_id = patient_id

class AppointmentSchema(ma.Schema):
    class Meta:
        fields = ('doctor_id','date','time_start','time_end', 'patient_id')

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many = True)

def add_patient(name, email):
    new_patient = Patient(name,email)
    db.session.add(new_patient)
    db.session.commit()

def get_patients():
    all_patients = Patient.query.all()
    return all_patients

def get_patient(id):
    patient = Patient.query.get(id)
    return patient

def add_doctor(name, email, major):
    new_doctor = Doctor(name,email,major)
    db.session.add(new_doctor)
    db.session.commit()

def get_doctors():
    all_doctors = Doctor.query.all()
    return all_doctors


def add_appointment(doctor_id, date, time_start, time_end, patient_id):
    new_appointment = Appointment(doctor_id, date, time_start, time_end, patient_id)
    db.session.add(new_appointment)
    db.session.commit()

def get_appointments():
    all_appointments = Appointment.query.all()
    return all_appointments

def get_appointment(id):
    appointment = Appointment.query.get(id)
    return all_appointment


