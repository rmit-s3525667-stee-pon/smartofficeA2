from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
import time
import sys
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
mod = Blueprint('doctor',__name__, template_folder='templates')

from smartoffice import model

appointments_html = "doctor_appointments.html"

def loginState():
    if 'type' in session:
        if session['type'] != "Doctor":
            return url_for('login')
        else:
            return None
    else: 
        return url_for('login')

# def convert_to_24(time):
#     return time[:-2] if time[-2:] == "AM" else str(int(time[:2]) + 12) + time[2:8] 

# read all appointments
@mod.route('/appointments')
def appointments():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    patients = model.get_patients()
    appointments = model.get_appointments_by_doctor(int(session['id']))
    data_output = {
        'patients':patients,
        'appointments':appointments,
        'content':appointments_html
    }

    return render_template('doctor_nav.html', **data_output)

# see appointments in calendar format
@mod.route('/calendar')
def calendar():
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	return render_template('doctor_nav.html', content = 'doctor_calendar.html')

# add an appointment
@mod.route('/appointments', methods=['POST'])
def add_appointments():
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	date = request.form['date']
	doctor_id = session['id']
	time_start = request.form['time_start']
	time_end = request.form['time_end']
	patient_id = None

	event_id = model.add_appointment_to_calendar(doctor_id, date, time_start, time_end, patient_id)
	model.add_appointment(doctor_id, date, time_start, time_end, patient_id, event_id)

	return redirect(url_for("doctor.add_appointments"))

@mod.route('/remove_appointment', methods=['POST'])
def remove_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    appointment_id = request.form['appointment_id']
    event_id = request.form['event_id']
    model.remove_appointment(appointment_id)
    model.remove_appointment_from_calendar(event_id)

    return redirect(url_for("doctor.add_appointments"))


