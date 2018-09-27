import requests
import json
from datetime import datetime


class Patient():
    def __init__(self, id, name, phone, birthday, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email

class Doctor():
    def __init__(self, id, name, major, email):
        self.id = id
        self.name = name
        self.major = major
        self.email = email

class Clerk():
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
class Appointment():
    def __init__(self, id, doctor_id, date, time_start, time_end, patient_id, event_id):
        self.id = id
        self.doctor_id = doctor_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.patient_id = patient_id
        self.event_id = event_id

class Availability():
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

    # add patient to the system
def add_patient(name, phone, birthday, email):
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
    # get all the patients
def get_patients():
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
    # get all the doctor
def get_doctors():
    url = URL + doctor_code
    doctors = []
    try: 
        response = requests.get(url)
        json_data = response.json()
        for doctor_json in json_data:
            doctor = Doctor(doctor_json['id'], doctor_json['name'], doctor_json['email'], doctor_json['major'])
            doctors.append(doctor)
        return doctors
        print("Doctors Retrieved")
    except:
        print("Unable to get doctors, Error Occur")
        return None

    # add doctor to the system
def add_doctor(name, email, major):
    url = URL + doctor_code
    data_send = {
        "name": name,
        "email": email,
        "major":major
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

def get_doctor(id):
    url = URL + doctor_code + "/"+ str(id)
    try:
        response = requests.get(url)
        json_data = response.json()
        doctor = Doctor(json_data['id'], json_data['name'], json_data['major'], json_data['email'])
        print("Doctor retrieve")
        return doctor
    except:
        print("Error Occur")
        return None

# get all the clerks
def get_clerks():
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

  # add clerk to the system
def add_clerk(name, email):
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


def get_clerk(id):
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
    # add a appointment
def add_appointment(doctor_id, date, time_start, time_end, patient_id, event_id):
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

    # Get All Appointments
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

def remove_appointment(id):
    url = URL + appointment_code + "/" + str(id)
    try:
        response = requests.delete(url)
        return True
    except:
        print("Cannot delete appointment, Error Occur")
        return False

def get_available_appointments():
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

def get_available_appointments_by_doctor(id):
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

def get_available_appointments_by_patient(id):
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

def get_appointments_by_patient(id):
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

def get_appointments_by_doctor(id):
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

def get_upcoming_appointments_by_doctor(id):
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

def book_appointment(appointment_id, patient_id):
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

def unbook_appointment(appointment_id):
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
def add_availability(doctor_id, date, time_start, time_end, event_id):
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

def get_availability():
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

def remove_availability(id):
    url = URL + availability_code + "/" + str(id)
    try: 
        response = requests.delete(url)
        print("Remove Availability")
        return True
    except:
        print("Unable to remove availability, Error Occur")
        return False

# Calendar API Caller

def remove_from_calendar(id):
    url = URL + calendar_code + "/" + str(id)
    try:
        response = requests.delete(url)
        print("Remove Event")
        return True
    except:
        print("Unable to remove event, Error Occur")
        return False

def add_to_calendar(summary, doctor_id, date, time_start, time_end):
    url = URL + calendar_code
    data_send = {
        "summary": summary,
        "doctor_id": doctor_id,
        "date": date,
        "time_start": time_start,
        "time_end": time_end
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