from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from smartoffice import db, ma
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/home/pi/A2/smartoffice/smartoffice/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
google_calendar_id = 'ujb115kig589rtaa9ecorfvfjo@group.calendar.google.com'


class Patient(db.Model):
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
    event_id = db.Column(db.String, unique=False)

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

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, unique = False)
    patient_id = db.Column(db.Integer, unique = False)
    appointment_id = db.Column(db.Integer, unique = True)
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

class Availability(db.Model):
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

def add_patient(name, phone, birthday, email):
    new_patient = Patient(name, phone, birthday, email)
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

def get_doctor(id):
    doctor = Doctor.query.get(id)
    return doctor

def add_appointment(doctor_id, date, time_start, time_end, patient_id, event_id):
    new_appointment = Appointment(doctor_id, date, time_start, time_end, patient_id,event_id)
    db.session.add(new_appointment)
    db.session.commit()

def add_availability(doctor_id, date, time_start, time_end, event_id):
    new_availability = Availability(doctor_id, date, time_start, time_end, event_id)
    db.session.add(new_availability)
    db.session.commit()

# summary can be Availability or Appointment
def add_to_calendar(summary, doctor_id, date, time_start, time_end):
    year, month, day = map(int, date.split('-'))
    startHour, startMinute = map(int, time_start.split(':'))
    endHour, endMinute = map(int, time_end.split(':'))

    start_time = datetime.datetime(year, month, day, startHour, startMinute)
    end_time = datetime.datetime(year, month, day, endHour, endMinute)

    time_start = start_time.strftime('%Y-%m-%dT%H:%M:%S+10:00')
    time_end   = end_time.strftime('%Y-%m-%dT%H:%M:%S+10:00')

    event = {
        'summary': summary,
        'location': 'Clinic',
        'transparency': 'transparent',
        'start': {
            'dateTime': time_start,
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': time_end,
            'timeZone': 'Australia/Melbourne',
        },
        'attendees': [
            {'email': 'doctor@clinic.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 5},
                {'method': 'popup', 'minutes': 10},
            ],
        }
    }
    event = service.events().insert(calendarId=google_calendar_id, body=event).execute()
    return event['id']

def get_appointment(id):
    appointment = Appointment.query.get(id)
    return all_appointment

def get_appointments():
    all_appointments = Appointment.query.order_by(Appointment.date, Appointment.time_start).all()
    return all_appointments

def remove_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id)
    appointment.delete()
    db.session.commit()

def get_availability():
    all_availabilities = Availability.query.order_by(Availability.date, Availability.time_start).all()
    return all_availabilities

def get_availability_by_doctor(id):
    all_availabilities = Availability.query.filter(Availability.doctor_id == id).order_by(Availability.date, Availability.time_start).all()
    return all_availabilities

def remove_availability(availability_id):
    appointment = Availability.query.filter_by(id=availability_id)
    appointment.delete()
    db.session.commit()   

def remove_from_calendar(event_id):
    service.events().delete(calendarId=google_calendar_id, eventId=event_id).execute()

def get_available_appointments():
    appointments = Appointment.query.filter(Appointment.patient_id == None).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_available_appointments_by_doctor(id):
    appointments = Appointment.query.filter(Appointment.patient_id == None).filter(Appointment.doctor_id == id).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_appointments_by_doctor(id):
    appointments = Appointment.query.filter(Appointment.doctor_id == id).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_appointments_by_patient(id):
    appointments = Appointment.query.filter(Appointment.patient_id == id).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_upcoming_appointments_by_doctor(id):
    now = datetime.datetime.now()
    currentdate = now.strftime("%Y-%m-%d")

    appointments = Appointment.query.filter(Appointment.doctor_id == id).filter(Appointment.date >= currentdate).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

# def get_past_appointments_by_doctor(id):

# def get_upcoming_appointments_by_patient(id):

# def get_past_appointments_by_patient(id):


def book_appointment(appointment_id, patient_id):
    appointment = Appointment.query.get(appointment_id)
    appointment.patient_id = patient_id
    db.session.commit()

def unbook_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    appointment.patient_id = None
    db.session.commit()





