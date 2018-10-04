from flask import Blueprint
from flask import Flask,session, render_template, url_for, redirect, request
import datetime
import sys
# Pi's directory
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
# Bram's directory
#sys.path.insert(0,'/Users/BramanthaPatra/A2Git/smartofficeA2/smartoffice/smartoffice')
# April's directory 
# sys.path.insert(0,'/Users/User/Downloads/smartoffice/smartofficeA2/smartoffice/smartoffice')
mod = Blueprint('clerk',__name__,  template_folder='templates')

from smartoffice import api_caller

clerk_book_appointment_html = "clerk_book_appointment.html"
clerk_patient_appointment_html = "clerk_patient_appointment.html"
make_appointment_html = "book_appointment.html"
appointments_html = "appointments.html"
show_appointment_html = "clerkdashboard.html"
profile_html = "profile.html"
clerk_html = "clerkdashboard.html"
patient_html = "patient.html"


def loginState():
    if 'type' in session:
        if session['type'] != "Clerk":
            return url_for('login')
        else:
            return None
    else: 
        return url_for('login')

@mod.route('/clerkdashboard', methods=['GET', 'POST'])
def clerkdashboard():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    if request.method == 'POST':
        patient_id = request.form['patient_name']
        appointment_id = request.form['appointment_id']
        api_caller.book_appointment(appointment_id, patient_id)

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

    patients = api_caller.get_patients()
    doctors = api_caller.get_doctors()
    appointments = api_caller.get_appointments()
    data_output = {
        'patients':patients,
        'doctors': doctors,
        'dates': dates,
        'days': days,
        'appointments':appointments,
        'content':show_appointment_html
    }

    return render_template('clerk.html', **data_output)


@mod.route('/appointments')
def appointments():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    doctors = api_caller.get_doctors()
    appointments = api_caller.get_appointments_by_patient(int(session['id']))

    data_output = {
        'doctors':doctors,
        'appointments':appointments,
        'content':appointments_html
    }

    return render_template("clerk.html", **data_output)

# @mod.route('/make_appointment', methods=['GET', 'POST'])
# def make_appointment():
#     redirect_link = loginState()
#     if redirect_link != None:
#         return redirect(redirect_link)

#     if request.method == 'GET':
#         appointments = api_caller.get_available_appointments()
#     elif request.method == 'POST':
#         doctor_id = request.form['doctor_name']
#         appointments = api_caller.get_available_appointments_by_doctor(doctor_id)

#     doctors = api_caller.get_doctors()
#     data_output = {
#         'doctors':doctors,
#         'appointments':appointments,
#         'content':make_appointment_html
#     }

#     return render_template("patient.html", **data_output)
@mod.route('/make_appointment', methods=['GET', 'POST'])
def make_appointment():
    # redirect_link = loginState()
    # if redirect_link != None:
    #     return redirect(redirect_link)

    if request.method == 'GET':
        appointments = api_caller.get_available_appointments()
    elif request.method == 'POST':
        patient_id = request.form['patient_name']
        appointments = api_caller.get_available_appointments_by_doctor(int(patient_id))

    patients = api_caller.get_patients()
    doctors = api_caller.get_doctors()
    data_output = {
        'patients':patients,
        'doctors':doctors,
        'appointments': appointments,
        'content': clerk_book_appointment_html
    }

    return render_template("clerk.html", **data_output)

@mod.route('/book_appointment', methods=['POST'])
def book_appointment():
    # redirect_link = loginState()
    # if redirect_link != None:
    #     return redirect(redirect_link)
    
    patient_id = session['id']
    appointment_id = request.form['appointment_id']
    api_caller.book_appointment(appointment_id, patient_id)
    

    return redirect(url_for("clerk.book_appointment"))

@mod.route('/unbook_appointment', methods=['POST'])
def unbook_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    appointment_id = request.form['appointment_id']
    api_caller.unbook_appointment(appointment_id)

    return redirect(url_for("clerk.clerkdashboard"))

