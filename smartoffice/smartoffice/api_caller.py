"""This module contains functions that make requests to the API"""

import requests
import json
from datetime import datetime


class Patient():
    """
    Initialise Patient. 

    A patient has id, name, phone, birthday and email
    """
    def __init__(self, id, name, phone, birthday, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email

class Doctor():
    """
    Initialise doctor.

    A doctor has id, name, email, major and an
    unique calendar
    """
    def __init__(self, id, name, email, major, calendar_id):
        self.id = id
        self.name = name
        self.major = major
        self.email = email
        self.calendar_id = calendar_id

class Clerk():
    """
    Initialise clerk
    
    Clerk has id, name and email
    """
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
class Appointment():
    """
    Initialise the appointment model

    An appointment contain id, doctor's id, patient's id
    event id, time start and end
    """
    def __init__(self, id, doctor_id, date, time_start, time_end, patient_id, event_id):        
        self.id = id
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.patient_id = patient_id
        self.event_id = event_id

class Availability():
    """
    Initialise doctor's availability model
    
    Doctor's availability has date, event id, time
    start and end.
    """
    def __init__(self, id, doctor_id, date, time_start, time_end, event_id):
        self.id = id
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.event_id = event_id
        

URL = 'http://10.132.80.171/'
patient_code = 'patient'
doctor_code = 'doctor'
clerk_code = 'clerk'
appointment_code = 'appointment'
availability_code = 'availability'
calendar_code = 'calendar'


# Patient API caller
def get_patient(id):
    """Get a patient using the API"""
    url = URL + patient_code + "/"+ str(id)
    try:
        response = requests.get(url)
        json_data = response.json()
        patient = Patient(json_data['id'], json_data['name'], json_data['phone'], json_data['birthday'], json_data['email'])
        print("Patient retrieve")
        return patient
    except:
        print("Error Occur")
        return None

# Add patient to the system
def add_patient(name, phone, birthday, email):
    """This function is used to add patient to the database"""
    url = URL + patient_code
    data_send = {
        "name": name,
        "phone": phone,
        "birthday": birthday,
        "email": email
    }
    try:
        response = requests.post(url, 
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
        )
        print("Patient added to the system")
        return True
    except:
        print("Unable to add patient, Error Occur")
        return False

# Get all the patients
def get_patients():
    """Get and return all patient from the database"""
    url = URL + patient_code
    patients = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for patient_json in json_data:
            patient = Patient(patient_json['id'], patient_json['name'], patient_json['phone'], patient_json['birthday'], patient_json['email'])
            patients.append(patient)
        print("Patients retrieved")
        return patients
    except:
        print("Unable to get patients, Error Occur")
        return None

# Doctor API caller
# Get all the doctor
def get_doctors():
    """This function gets and return all doctors from the database"""
    url = URL + doctor_code
    doctors = []
    try: 
        response = requests.get(url)
        json_data = response.json()
        for doctor_json in json_data:
            doctor = Doctor(doctor_json['id'], doctor_json['name'], doctor_json['email'], doctor_json['major'], doctor_json['calendar_id'])
            doctors.append(doctor)
        return doctors
        print("Doctors Retrieved")
    except:
        print("Unable to get doctors, Error Occur")
        return None

# Add doctor to the system
def add_doctor( name, major, email, calendar_id):
    """Add doctor to the database"""
    url = URL + doctor_code
    data_send = {
        "name": name,
        "major":major,
        "email": email,
        "calendar_id":None
    }
    try:
        response = requests.post(url, 
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
        )
        print("Doctor added to the system")
        return True
    except:
        print("Unable to add doctor, Error Occur")
        return False

# Get a specific doctor
def get_doctor(id):
    """Get a specific doctor by calling the doctor's id"""
    url = URL + doctor_code + "/"+ str(id)
    doctors = []
    try:
        response = requests.get(url)
        json_data = response.json()
        doctor = Doctor(json_data['id'], json_data['name'], json_data['email'], json_data['major'], json_data['calendar_id'])
        return doctor
        print("Doctor retrieve")
    except:
        print("Error Occur")
        return None

# Get all the clerks
def get_clerks():
    """Get and return all the clerks from the system"""
    url = URL + clerk_code
    clerks = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for clerk_json in json_data:
            clerk = Clerk(clerk_json['id'], clerk_json['name'], clerk_json['email'])
            clerks.append(clerk)
        print("Clerks retrieved")
        return clerks
    except:
        print("Unable to get clerks, Error Occur")
        return None

# Add clerk to the system
def add_clerk(name, email):
    """Add clerk to the database"""
    url = URL + clerk_code
    data_send = {
        "name": name,
        "email": email,
    }
    try:
        response = requests.post(url, 
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
        )
        print("Clerk added to the system")
        return True
    except:
        print("Unable to add clerk, Error Occur")
        return False

# Get a specific clerk
def get_clerk(id):
    """Get a specific clerk by that clerk's id"""
    url = URL + clerk_code + "/"+ str(id)
    try:
        response = requests.get(url)
        json_data = response.json()
        clerk = Clerk(json_data['id'], json_data['name'], json_data['email'])
        print("Clerk retrieve")
        return clerk
    except:
        print("Error Occur")
        return None

# Appointment API Caller
# Add a appointment
def add_appointment(doctor_id, date, time_start, time_end, patient_id, event_id):
    """Add an appointment to the system"""
    url = URL + appointment_code
    data_send = {
        "doctor_id": doctor_id,
        "date": date,
        "time_start": time_start,
        "time_end": time_end,
        "patient_id": patient_id,
        "event_id": event_id
    }
    try:
        response = requests.post(url,
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
        )
        print("Appointment have been added")
        return True
    except:
        print("Unable to add Appointment, Error Occur")
        return False

# Get all appointments
def get_appointments():
    url = URL + appointment_code
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['doctor_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['patient_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Get Appointment by Id        
def get_appointment(id):
    """
    Get an appointment from doctor or patient
    by the appointment id
    """
    url = URL + appointment_code + "/"+ str(id)
    try:
        response = requests.get(url)
        json_data = response.json()
        appointment = Appointment(json_data['id'],
            json_data['doctor_id'], json_data['date'], 
            json_data['time_start'], json_data['time_end'], 
            json_data['patient_id'], json_data['event_id']
            )
        print("Retrieve Appointment")
        return appointment
    except:
        print("Unable to get Appointment, Error Occur")
        return None

# Remove an appointment
def remove_appointment(id):
    """Remove the appointment by its id"""
    url = URL + appointment_code + "/" + str(id)
    try:
        response = requests.delete(url)
        return True
    except:
        print("Cannot delete appointment, Error Occur")
        return False

# Get all available appointments
def get_available_appointments():
    """
    Get all of the appoinments that is still
    available to allocate.
    """
    url = URL + appointment_code + "/available"
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['doctor_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['patient_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Get available apointment by doctor
def get_available_appointments_by_doctor(id):
    """
    Get all of the available appointment
    that has not been allocated by doctor's id
    """
    url = URL + appointment_code + "/available/doctor/" + str(id)
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['doctor_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['patient_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Get available appointment by patient
def get_available_appointments_by_patient(id):
    """
    Get all of the available appointment
    that has not been allocated by patient's id
    """
    url = URL + appointment_code + "/available/patient/" + str(id)
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['patient_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['doctor_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Get the scheduled appointments by patient
def get_appointments_by_patient(id):
    """
    Get the appointments that has been allocated by patient's id -
    or in another way, a list of patient's scheduled appointments 
    """
    url = URL + appointment_code + "/patient/" + str(id)
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['doctor_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['patient_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Get the scheduled appointments by doctor
def get_appointments_by_doctor(id):
    """
    Get a list of doctor's scheduled appointments 
    by doctor's id
    """
    url = URL + appointment_code + "/doctor/" + str(id)
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['doctor_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['patient_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Get the upcoming doctor's appointments 
def get_upcoming_appointments_by_doctor(id):
    """Get doctor's next scheduled appointments"""
    url = URL + appointment_code + "/doctor/next/" + str(id)
    appointments = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for appointment_json in json_data:
            appointment = Appointment(appointment_json['id'],
                appointment_json['doctor_id'], appointment_json['date'], 
                appointment_json['time_start'], appointment_json['time_end'], 
                appointment_json['patient_id'], appointment_json['event_id']
                )
            appointments.append(appointment)
        print("Retrieve Appointments")
        return appointments
    except:
        print("Unable to get Appointments, Error Occur")
        return None

# Book appointment
def book_appointment(appointment_id, patient_id):
    """
    Get the available appointment id and patient id 
    then allocate the patient with that appointment 
    """
    url = URL + appointment_code + "/book"
    data_send = {
        "appointment_id": appointment_id,
        "patient_id": patient_id
    }
    try:
        response = requests.put(url,
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
        )
        print("Appointment Booked")
        return True
    except:
        print("Unable to Book the appointment, Error Occur")
        return False

# Unbook an appointment
def unbook_appointment(appointment_id):
    """
    Update the appointment, removing the patient's id
    so the appointment becomes available 
    """
    url = URL + appointment_code + "/unbook"
    data_send = {
        "appointment_id": appointment_id
    }
    try:
        response = requests.put(url,
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
        )
        print("Appointment Unbooked")
        return True
    except:
        print("Unable to Unbook the appointment, Error Occur")
        return False



# Availability API Caller
# Add doctor's availability
def add_availability(doctor_id, date, time_start, time_end, event_id):
    """
    Add doctor's availbility to the system
    by adding date, time start and end
    """
    url = URL + availability_code
    data_send = {
        "doctor_id": doctor_id,
        "date": date,
        "time_start": time_start,
        "time_end": time_end,
        "event_id": event_id
    }
    try:
        response = requests.post(url,
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
            )
        print("Availability Added to the system")
        return True
    except:
        print("Unable to add Availability to the system, Error Occur")
        return False

# Get doctor's availability
def get_availability():
    """
    Get and return doctor's list of availability
    """
    url = URL + availability_code
    availabilities = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for avail_json in json_data:
            availability = Availability(avail_json['id'], avail_json['doctor_id'],
                avail_json['date'], avail_json['time_start'], avail_json['time_end'],
                avail_json['event_id']
                )
            availabilities.append(availability)
        print("Retrieve Availabilities")
        return availabilities
    except:
        print("Unable to retrieve availabilities, Error Occur")
        return None

#############################
def get_availability_by_doctor(id):
    url = URL + availability_code + "/doctor/" + str(id)
    availabilities = []
    try:
        response = requests.get(url)
        json_data = response.json()
        for avail_json in json_data:
            availability = Availability(avail_json['id'], avail_json['doctor_id'],
                avail_json['date'], avail_json['time_start'], avail_json['time_end'],
                avail_json['event_id']
                )
            availabilities.append(availability)
        print("Retrieve Availabilities")
        return availabilities
    except:
        print("Unable to retrieve availabilities, Error Occur")
        return None

# Remove doctor's availability
def remove_availability(id):
    """Remove doctor's availability by availability session id"""
    url = URL + availability_code + "/" + str(id)
    try: 
        response = requests.delete(url)
        print("Remove Availability")
        return True
    except:
        print("Unable to remove availability, Error Occur")
        return False

# Calendar API Caller

# Remove event (booked appointment) on the calendar
def remove_from_calendar(id):
    """Remove the appointment from the calendar"""
    url = URL + calendar_code + "/" + str(id)
    try:
        response = requests.delete(url)
        print("Remove Event")
        return True
    except:
        print("Unable to remove event, Error Occur")
        return False

# Add event to the calendar
def add_to_calendar(summary, doctor_id, date, time_start, time_end, calendar_id):
    """Send the data and add the event to the Google Calendar"""
    url = URL + calendar_code
    data_send = {
        "summary": summary,
        "doctor_id": doctor_id,
        "date": date,
        "time_start": time_start,
        "time_end": time_end,
        "calendar_id": calendar_id
    }
    try:
        response = requests.post(url,
            data = json.dumps(data_send),
            headers = {'Content-Type':'application/json'}
            )
        print("A new event added to Calendar")
        return True
    except:
        print("Unable to add event into the Calendar, Error Occur")