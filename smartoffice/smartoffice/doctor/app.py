from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request, flash
import time, datetime, json, calendar
import sys
# Pi's directory
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
# Bram's directory
#sys.path.insert(0,'/Users/BramanthaPatra/A2Git/smartofficeA2/smartoffice/smartoffice')
# April's directory 
# sys.path.insert(0,'/Users/User/Downloads/smartoffice/smartofficeA2/smartoffice/smartoffice')

mod = Blueprint('doctor',__name__, template_folder='templates')

from smartoffice import api_caller

appointments_html = "doctor_appointments.html"
calendar_html = "doctor_calendar.html"
patient_record_html = "medical_record.html"
upcoming_appointments_html = "upcoming_appointments.html"
all_appointments_html = "all_appointments.html"

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

    index = 0
    today = datetime.datetime.today()
    today_str = today.isoweekday()
    distance_to_sunday = 7 - today.isoweekday()
    dates = [0] * (distance_to_sunday + 7)
    days = [0] * (distance_to_sunday + 7)

    for index in range(0, 7):
    	curr_date = today + datetime.timedelta(days=index +  distance_to_sunday)
    	dates.insert(index, datetime.datetime.strftime(curr_date, "%Y-%m-%d"))
    	days.insert(index, datetime.datetime.strftime(curr_date, "%A"))

    patients = api_caller.get_patients()
    availabilities = api_caller.get_availability_by_doctor(int(session['id']))
    doctors = api_caller.get_doctor(int(session['id']))
    data_output = {
        'patients':patients,
        'availabilities': availabilities,
        'doctors': doctors,
        'dates' : dates,
        'days': days,
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

# see availabilities in calendar format
@mod.route('/upcoming_appointments', methods=['GET', 'POST'])
def upcoming_appointments():
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	if request.method == 'POST':
		patient_id = request.form['patient_id']
		return redirect(url_for("doctor.patient_record", id = patient_id))

	doctors = api_caller.get_doctor(int(session['id']))
	appointments = api_caller.get_upcoming_appointments_by_doctor(int(session['id']))
	data_output = {
        'doctors': doctors,
        'appointments': appointments,
        'content':upcoming_appointments_html
    }

	return render_template('doctor_nav.html', **data_output)

@mod.route('/all_appointments', methods=['GET', 'POST'])
def all_appointments():
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	if request.method == 'GET':
		appointments = api_caller.get_appointments_by_doctor(int(session['id']))
		show_individual = None
	elif request.method == 'POST':
		input_date = request.form['input_date']
		show_individual = True
		appointments = api_caller.get_appointments_by_doctor_and_date(int(session['id']), input_date)

	index = 0
	today = datetime.datetime.today()
	today_str = today.isoweekday()
	distance_to_sunday = 7 - today.isoweekday()
	dates = [0] * (distance_to_sunday + 7)
	days = [0] * (distance_to_sunday + 7)

	for index in range(0, 7 + distance_to_sunday):
		curr_date = today + datetime.timedelta(days=index)
		dates.insert(index, datetime.datetime.strftime(curr_date, "%Y-%m-%d"))
		days.insert(index, datetime.datetime.strftime(curr_date, "%A"))

	doctors = api_caller.get_doctor(int(session['id']))
	patients = api_caller.get_patients()
	data_output = {
	'doctors': doctors,
	'appointments': appointments,
	'show_individual': show_individual,
	'dates': dates,
	'patients': patients,
	'days': days,
	'content':all_appointments_html
	}

	return render_template('doctor_nav.html', **data_output)


# add an availability
@mod.route('/add_availability', methods=['POST'])
def add_availability():
	today = datetime.datetime.now()
	distance_to_sunday = 7 - today.isoweekday()
	eotw = today + datetime.timedelta(days=distance_to_sunday)
	eonw = eotw + datetime.timedelta(days=7 + distance_to_sunday)

	end_of_this_week = eotw.strftime("%Y-%m-%d")
	end_of_next_week = eonw.strftime("%Y-%m-%d")

	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)

	# form = ReusableFormAvailability(request.form)
	# print (form.errors)

	# if form.validate() :
	date = request.form['date']
	doctor_id = session['id']
	time_start = request.form['time_start']
	time_end = request.form['time_end']
	summary = request.form['doctor_name']
	calendar_id = request.form['doctor_calendar_id']

	if end_of_this_week < date <= end_of_next_week :
		event_id = api_caller.add_to_calendar(summary,doctor_id, date, time_start, time_end, calendar_id)
		api_caller.add_availability(doctor_id, date, time_start, time_end, event_id)
		add_appointment_automatically(doctor_id, date, time_start, time_end, calendar_id)
		flash('Availability is successfully added')
		return redirect(url_for("doctor.availabilities"))
	else:
		flash('Error: You can only add availability for next week')
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
    event_id = request.form['event_id']
    calendar_id = request.form['calendar_id']

    api_caller.remove_availability(availability_id)
    api_caller.remove_from_calendar(calendar_id, event_id)

    remove_appoinment_automatically(calendar_id, doctor_id, date, time_start)

    return redirect(url_for("doctor.availabilities"))


@mod.route('/medical_record/<id>')
def patient_record(id):
	redirect_link = loginState()
	if redirect_link != None:
		return redirect(redirect_link)


	patient = api_caller.get_patient(id)
	records = api_caller.get_patient_medical_record(id)
	doctor = api_caller.get_doctor(session['id'])
	doctors = api_caller.get_doctors()
	date = datetime.datetime.now()
	date = datetime.datetime.strftime(date, "%Y-%m-%d")
	data_output = {
		'date':date,
		'records':records,
		'patient':patient,
		'doctor':doctor,
		'doctors':doctors,
        'content':patient_record_html
    }
	return render_template('doctor_nav.html', **data_output)

@mod.route('medical_record',methods=['POST'])
def add_record():
	doctor_id = session['id']
	patient_id = request.form['patient_id']
	notes = request.form['notes']
	api_caller.add_medical_record(doctor_id, patient_id, notes)
	return redirect(url_for("doctor.patient_record", id = patient_id))

def remove_appoinment_automatically(calendar_id, doctor_id, date, time_start):

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
					api_caller.remove_from_calendar(calendar_id, app['event_id'])
					st = st + datetime.timedelta(minutes = 15)
					time_start_format = datetime.datetime.strftime(st, '%H:%M:%S')






