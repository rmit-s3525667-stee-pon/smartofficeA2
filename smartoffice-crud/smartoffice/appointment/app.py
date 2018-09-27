from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
import time
import sys
sys.path.insert(0,'/home/pi/playground/smartofficeA2/smartoffice-crud/smartoffice')
mod = Blueprint('appointment',__name__, template_folder='templates')

from smartoffice import model

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

# Add appointment
@mod.route('', methods=['POST'])
def add_appointments():
    doctor_id = request.json['doctor_id']
    date = request.json['date']
    time_start = request.json['time_start']
    time_end = request.json['time_end']
    patient_id = request.json['patient_id']
    event_id = request.json['event_id']
    new_appointment = model.add_appointment(doctor_id, date, time_start, time_end, patient_id, event_id)
    return model.appointment_schema.jsonify(new_appointment)

# Get All Appointments
@mod.route('', methods=['GET'])
def get_appointments():
    appointments = model.get_appointments()
    return model.appointments_schema.jsonify(appointments)

# Get Appointment by Id
@mod.route('/<id>', methods=['GET'])
def get_appointment(id):
    appointment = model.get_appointment(id)
    return appointment_schema.jsonify(appointment)

# Remove Appointment by Id
@mod.route('/<id>', methods=['DELETE'])
def remove_appointment(id):
    if model.remove_appointment(id):
        return True
    else:
        return False

# Get All Available Appointments
@mod.route('/available', methods=['GET'])
def get_available_appointments():
    appointments = model.get_available_appointments()
    return model.appointments_schema.dumps(appointments, default = date_handler )


# Get All Available Appoinments of a Doctor by Doctor Id
@mod.route('/available/doctor/<id>', methods=['GET'])
def get_available_appointments_by_doctor(id):
    appointments = model.get_available_appointments_by_doctor(id)
    return model.appointments_schema.jsonify(appointments)

# Get All Appoinments of a Patient by Patient Id
@mod.route('/patient/<id>', methods=['GET'])
def get_appointments_by_patient(id):
    appointments = model.get_appointments_by_patient(id)
    return model.appointments_schema.jsonify(appointments)

# Get All Appointent of a Doctor
@mod.route('/doctor/<id>', methods=['GET'])
def get_appointments_by_doctor(id):
    appointments = model.get_appointments_by_doctor(id)
    return model.appointments_schema.jsonify(appointments)

# Get All Upcoming Appoinments of a Doctor
@mod.route('/doctor/next/<id>', methods=['GET'])
def get_upcoming_appoinments_by_doctor(id):
    print("hello")
    appointments = model.get_upcoming_appointments_by_doctor(id)
    print(appointments)
    return model.appointments_schema.jsonify(appointments)

# Book An Appointment
@mod.route('/book', methods=['PUT'])
def book_appointment():
    appointment_id = request.json['appointment_id']
    patient_id = request.json['patient_id']
    appointment = model.book_appointment(appointment_id, patient_id)
    return model.appointment_schema.jsonify(appointment)

# UnBook An Appointment
@mod.route('/unbook', methods=['PUT'])
def unbook_appointment():
    appointment_id = request.json['appointment_id']
    appointment = model.unbook_appointment(appointmen_id)
    return model.appointment_schema.jsonify(appointment)