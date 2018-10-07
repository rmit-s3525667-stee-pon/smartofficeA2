"""This module contain functions and class that directly communicate with the database"""

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
store = file.Storage('/Users/giang/Desktop/SOA2/smartofficeA2/smartoffice-crud/smartoffice/token.json')
creds = store.get()
if not creds or creds.invalid:
    # Minh's pi
    # flow = client.flow_from_clientsecrets('/home/pi/playground/smartofficeA2/smartoffice-crud/smartoffice', SCOPES)
    # Bram and April's pi
    flow = client.flow_from_clientsecrets('/Users/giang/Desktop/SOA2/smartofficeA2/smartoffice-crud/smartoffice/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
google_calendar_id = 'ujb115kig589rtaa9ecorfvfjo@group.calendar.google.com'


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

def add_patient(name, phone, birthday, email):
    """Add Patient"""
    new_patient = Patient(name, phone, birthday, email)
    db.session.add(new_patient)
    db.session.commit()

def get_patients():
    """Get All Patients"""
    all_patients = Patient.query.all()
    return all_patients

def get_patient(id):
    """Get Patient by Id"""
    patient = Patient.query.get(id)
    return patient

def add_doctor(name, email, major, calendar_id):
    """Add Doctor"""
    new_doctor = Doctor(name,major,email, calendar_id)
    db.session.add(new_doctor)
    db.session.commit()

def get_doctors():
    """Get All Doctors"""
    all_doctors = Doctor.query.all()
    return all_doctors

def get_doctor(id):
    """Get Doctor by ID"""
    doctor = Doctor.query.get(id)
    return doctor

def add_clerk(name, email):
    """Add Clerk"""
    new_clerk = Clerk(name,email)
    db.session.add(new_clerk)
    db.session.commit()

def get_clerks():
    """Get All Clerks"""
    all_clerks = Clerk.query.all()
    return all_clerks

def get_clerk(id):
    """Get Clerk by ID"""
    clerk = Clerk.query.get(id)
    return clerk
    
def add_appointment(doctor_id, date, time_start, time_end, patient_id, event_id):
    """Add Appointment"""
    new_appointment = Appointment(doctor_id, date, time_start, time_end, patient_id,event_id)
    db.session.add(new_appointment)
    db.session.commit()

def add_availability(doctor_id, date, time_start, time_end, event_id):
    """Add availability"""
    new_availability = Availability(doctor_id, date, time_start, time_end, event_id)
    db.session.add(new_availability)
    db.session.commit()

def add_calendar(summary):
    """Create a calendar in google calendar"""
    calendar = {
        'summary': summary,
        'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    return created_calendar['id']

# summary can be Availability or Appointment
def add_to_calendar(summary, doctor_id, date, time_start, time_end, calendar_id):
    """Add event to calendar"""
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
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event['id']


def remove_from_calendar(calendar_id, event_id):
    """Remove event from calendar"""
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


def get_appointment(id):
    """Get Appointment by ID"""
    appointment = Appointment.query.get(id)
    return appointment

def get_appointments():
    """Get All Appointments"""
    all_appointments = Appointment.query.order_by(Appointment.date, Appointment.time_start).all()
    return all_appointments

def remove_appointment(appointment_id):
    """Remove Appointment by ID"""
    try:
        appointment = Appointment.query.filter_by(id=appointment_id)
        appointment.delete()
        db.session.commit()
        return True
    except:
        return False


def get_availability():
    """Get availability"""
    all_availabilities = Availability.query.order_by(Availability.date, Availability.time_start).all()
    return all_availabilities

def get_availability_by_doctor(id):
    """Get availability by doctor ID"""
    all_availabilities = Availability.query.filter(Availability.doctor_id == id).order_by(Availability.date, Availability.time_start).all()
    return all_availabilities

def remove_availability(availability_id):
    """Remove availability"""
    appointment = Availability.query.filter_by(id=availability_id)
    appointment.delete()
    db.session.commit()   

def get_available_appointments():
    """Get All available appointments"""
    appointments = Appointment.query.filter(Appointment.patient_id == None).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_available_appointments_by_doctor(id):
    """Get available appointments by doctor ID"""
    appointments = Appointment.query.filter(Appointment.patient_id == None).filter(Appointment.doctor_id == id).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_appointments_by_doctor(id):
    """Get appointments by doctor ID"""
    appointments = Appointment.query.filter(Appointment.doctor_id == id).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_appointments_by_doctor_and_date(id, input_date):
    """Get available appointments by doctor ID and Date"""
    appointments = Appointment.query.filter(Appointment.doctor_id == id).filter(Appointment.date == input_date).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_appointments_by_patient(id):
    """Get appointment by Patient ID"""
    appointments = Appointment.query.filter(Appointment.patient_id == id).order_by(Appointment.date, Appointment.time_start).all()
    return appointments

def get_upcoming_appointments_by_doctor(id):
    """Get upcoming appointments by doctor ID"""
    now = datetime.datetime.now()
    distance_to_sunday = 7 - now.isoweekday()
    eow = now + datetime.timedelta(days=distance_to_sunday)
    end_of_week = eow.strftime("%Y-%m-%d")
    currentdate = now.strftime("%Y-%m-%d")

    appointments = Appointment.query.filter(Appointment.doctor_id == id).filter(end_of_week >= Appointment.date).order_by(Appointment.date, Appointment.time_start).all()
    return appointments


def book_appointment(appointment_id, patient_id):
    """Book appointment"""
    appointment = Appointment.query.get(appointment_id)
    appointment.patient_id = patient_id
    db.session.commit()
    return appointment

def unbook_appointment(appointment_id):
    """Unbook appointment"""
    appointment = Appointment.query.get(appointment_id)
    appointment.patient_id = None
    db.session.commit()
    return appointment

def add_medical_record(doctor_id, patient_id, date, notes):
    """Add medical record"""
    new_record = MedicalRecord(doctor_id, patient_id, date, notes)
    db.session.add(new_record)
    db.session.commit()

def get_patient_medical_record(id):
    """Get medical record by patient ID"""
    records = MedicalRecord.query.filter(MedicalRecord.patient_id == id).order_by(MedicalRecord.date).all()
    return records

def get_patient_by_name(name):
    """Get Patient by name"""
    patient = Patient.query.filter(Patient.name == name).first()
    return patient

def get_doctor_by_name(name):
    """Get Doctor by name"""
    doctor = Doctor.query.filter(Doctor.name == name).first()
    return doctor




