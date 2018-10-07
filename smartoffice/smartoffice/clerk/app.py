"""This module contain the route for all tabs in Clerk page"""

from flask import Blueprint
from flask import Flask,session, render_template, url_for, redirect, request
import datetime
import sys, json

# Pi's directory
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')

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
    """Check the current login status"""
    #Only the clerk allow to access this page
    if 'type' in session:
        if session['type'] != "Clerk":
            return url_for('login')
        else:
            return None
    else: 
        return url_for('login')

@mod.route('/clerkdashboard', methods=['GET', 'POST'])
def clerkdashboard():
    """Clerk dashboard page"""

    # Check the login status
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    if request.method == 'GET':
        appointments = api_caller.get_appointments()
   
    # Run when ever the clerk book appointment for patient
    elif request.method == 'POST':
        patient_id = request.form['patient_name']
        appointment_id = request.form['appointment_id']
        doctor_id = request.form['doctor_name']

        if patient_id != "None":
           api_caller.book_appointment(appointment_id, patient_id)
           appointments = api_caller.get_appointments()
        elif doctor_id != "None":
            appointments = api_caller.get_appointments_by_doctor(doctor_id)
        

    index = 0
    today = datetime.datetime.today()
    today_str = datetime.datetime.strftime(today, "%Y-%m-%d")
    distance_to_sunday = 7 - today.isoweekday()
    dates = [0] * (distance_to_sunday + 7)
    days = [0] * (distance_to_sunday + 7)
    two_week_days = 14

    for index in range(0, two_week_days):
        curr_date = today - datetime.timedelta(days=today.isoweekday()) + datetime.timedelta(days=index)
        dates.insert(index, datetime.datetime.strftime(curr_date, "%Y-%m-%d"))
        days.insert(index, datetime.datetime.strftime(curr_date, "%A"))

    # Retrieve data to display onto the webpage
    patients = api_caller.get_patients()
    doctors = api_caller.get_doctors()
    data_output = {
        'patients':patients,
        'doctors': doctors,
        'dates': dates,
        'today': today,
        'days': days,
        'appointments':appointments,
        'content':show_appointment_html
    }

    return render_template('clerk.html', **data_output)

@mod.route('/unbook_appointment', methods=['POST'])
def unbook_appointment():
    """Unbook the appointment for the patient"""
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    appointment_id = request.form['appointment_id']
    api_caller.unbook_appointment(appointment_id)

    return redirect(url_for("clerk.clerkdashboard"))

