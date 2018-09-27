from flask import Blueprint
from flask import Flask,session, render_template, url_for, redirect, request
import sys
sys.path.insert(0,'/Users/User/Downloads/smartoffice/smartofficeA2/smartoffice/smartoffice')
mod = Blueprint('clerk',__name__,  template_folder='templates')

from smartoffice import api_caller

make_appointment_html = "book_appointment.html"
appointments_html = "appointments.html"
show_appointment_html = "clerkdashboard.html"
profile_html = "profile.html"
clerk_html = "clerkdashboard.html"


def loginState():
    if 'type' in session:
        if session['type'] != "Clerk":
            return url_for('login')
        else:
            return None
    else: 
        return url_for('login')

@mod.route('/clerkdashboard')
def clerkdashboard():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    patients = api_caller.get_patients()
    appointments = api_caller.get_appointments_by_patient(int(session['id']))
    data_output = {
        'patients':patients,
        'appointments':appointments,
        'content':clerk_html
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

    return render_template("patient.html", **data_output)

@mod.route('/show_appointment', methods=['GET', 'POST'])
def show_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    if request.method == 'GET':
        appointments = api_caller.get_available_appointments()
    elif request.method == 'POST':
        patient_id = request.form['patient_name']
        appointments = api_caller.get_available_appointments_by_patient(patient_id)

    doctors = api_caller.get_doctors()
    appointments = api_caller.get_appointments_by_patient(int(session['id']))
    data_output = {
        'doctors':doctors,
        'appointments':appointments,
        'content':show_appointment_html
    }

    return render_template("clerkdashboard.html", **data_output)

@mod.route('/book_appointment', methods=['POST'])
def book_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    patient_id = session['id']
    appointment_id = request.form['appointment_id']
    api_caller.book_appointment(appointment_id, patient_id)

    return redirect(url_for("patient.appointments"))

@mod.route('/unbook_appointment', methods=['POST'])
def unbook_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    appointment_id = request.form['appointment_id']
    api_caller.unbook_appointment(appointment_id)

    return redirect(url_for("patient.appointments"))

