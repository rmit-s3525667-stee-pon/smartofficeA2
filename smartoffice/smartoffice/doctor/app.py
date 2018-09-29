from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
import time, datetime, json
import sys
# Pi's directory
# sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
# Bram's directory
sys.path.insert(0,'/Users/BramanthaPatra/A2Git/smartofficeA2/smartoffice/smartoffice')
# April's directory 
# sys.path.insert(0,'/Users/User/Downloads/smartoffice/smartofficeA2/smartoffice/smartoffice')

mod = Blueprint('doctor',__name__, template_folder='templates')

from smartoffice import api_caller

appointments_html = "doctor_appointments.html"
calendar_html = "doctor_calendar.html"

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

	doctors = api_caller.get_doctor(int(session['id']))
	data_output = {
        'doctors': doctors,
        'content':calendar_html
    }

	return render_template('doctor_nav.html', **data_output)

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
	calendar_id = request.form['doctor_calendar_id']

	event_id = api_caller.add_to_calendar(summary,doctor_id, date, time_start, time_end, calendar_id)
	api_caller.add_availability(doctor_id, date, time_start, time_end, event_id)

	add_appointment_automatically(doctor_id, date, time_start, time_end, calendar_id)

	return redirect(url_for("doctor.availabilities"))

def add_appointment_automatically(doctor_id, date, time_start, time_end, calendar_id):
	patient_id = None
	summary = "Appointment"

	st = datetime.datetime.strptime(time_start, '%H:%M')
	et = datetime.datetime.strptime(time_end, '%H:%M')
	tdelta = et - st

	num = int((tdelta.total_seconds()/3600) * 4)
	for x in range(num):
		time_end = st + datetime.timedelta(minutes = 15)
		time_end_format = datetime.datetime.strftime(time_end, '%H:%M')
		event_id = api_caller.add_to_calendar(summary,doctor_id, date, time_start, time_end_format, calendar_id)
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
    doctor_id = request.form['doctor_id']
    date = request.form['date']
    time_start = request.form['time_start']
    api_caller.remove_availability(availability_id)
    api_caller.remove_from_calendar(event_id)

    remove_appoinment_automatically(doctor_id, date, time_start)

    return redirect(url_for("doctor.availabilities"))


def remove_appoinment_automatically(doctor_id, date, time_start):

	appointments = api_caller.get_appointments()
	appointments_dumps = json.dumps(appointments, default=lambda o: o.__dict__, sort_keys=True, indent=4)
	appointments_loads = json.loads(appointments_dumps)


	st = datetime.datetime.strptime(time_start, '%H:%M:%S')
	time_start_format = datetime.datetime.strftime(st, '%H:%M:%S')


	for app in appointments_loads:
		if app['doctor_id'] == int(doctor_id):
			if app['date'] == date:
				if app['time_start'] == time_start_format:
					api_caller.remove_appointment(app['id'])
					st = st + datetime.timedelta(minutes = 15)
					time_start_format = datetime.datetime.strftime(st, '%H:%M:%S')






