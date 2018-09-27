from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
import time, datetime
import sys
# sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
sys.path.insert(0,'/Users/User/Downloads/smartoffice/smartofficeA2/smartoffice/smartoffice')
mod = Blueprint('doctor',__name__, template_folder='templates')

from smartoffice import api_caller

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

# read all availabilities
@mod.route('/availabilities')
def availabilities():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    patients = api_caller.get_patients()
    availabilities = api_caller.get_availability_by_doctor(int(session['id']))
    doctors = api_caller.get_doctor(int(session['id']))
    data_output = {
        'patients':patients,
        'availabilities': availabilities,
        'doctors': doctors,
        'content':appointments_html
    }

    return render_template('doctor_nav.html', **data_output)

# see availabilities in calendar format
@mod.route('/calendar')
def calendar():
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	return render_template('doctor_nav.html', content = 'doctor_calendar.html')

# add an availability
@mod.route('/add_availability', methods=['POST'])
def add_availability():
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	date = request.form['date']
	doctor_id = session['id']
	time_start = request.form['time_start']
	time_end = request.form['time_end']
	summary = request.form['doctor_name']

	event_id = api_caller.add_to_calendar(summary,doctor_id, date, time_start, time_end)
	api_caller.add_availability(doctor_id, date, time_start, time_end, event_id)

	add_appointment_automatically(doctor_id, date, time_start, time_end)

	return redirect(url_for("doctor.availabilities"))

def add_appointment_automatically(doctor_id, date, time_start, time_end):
	patient_id = None
	summary = "Appointment"

	st = datetime.datetime.strptime(time_start, '%H:%M')
	et = datetime.datetime.strptime(time_end, '%H:%M')
	tdelta = et - st
	fifteen_mins = datetime.datetime.strptime('00:15', '%H:%M')

	num = int((tdelta.total_seconds()/3600) * 4)
	for x in range(num):
		time_end = st + datetime.timedelta(minutes = 15)
		time_end_format = datetime.datetime.strftime(time_end, '%H:%M')
		event_id = api_caller.add_to_calendar(summary,doctor_id, date, time_start, time_end_format)
		api_caller.add_appointment(doctor_id, date, time_start, time_end_format, patient_id, event_id)

		# time_end_strptime = datetime.datetime.strptime(time_end, '%Y %m %d %H:%M:%S')
		time_start = time_end
		time_start = datetime.datetime.strftime(time_start, '%H:%M')
		st = datetime.datetime.strptime(time_start, '%H:%M')

# remove an availability
@mod.route('/remove_availability', methods=['POST'])
def remove_availability():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    availability_id = request.form['availability_id']
    event_id = request.form['event_id']
    api_caller.remove_availability(availability_id)
    api_caller.remove_from_calendar(event_id)

    return redirect(url_for("doctor.availabilities"))


