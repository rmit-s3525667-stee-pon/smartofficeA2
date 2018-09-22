from flask import Blueprint
from flask import Flask,session, render_template, url_for, redirect, request
import sys
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
mod = Blueprint('patient',__name__,  template_folder='templates')

from smartoffice import model

make_appointment_html = "book_appointment.html"
appointments_html = "appointments.html"
profile_html = "profile.html"


def loginState():
    if 'type' in session:
        if session['type'] != "Patient":
            return url_for('login')
        else:
            return None
    else: 
        return url_for('login')

@mod.route('/appointments')
def appointments():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    doctors = model.get_doctors()
    appointments = model.get_appointments_by_patient(int(session['id']))

    data_output = {
        'doctors':doctors,
        'appointments':appointments,
        'content':appointments_html
    }

    return render_template("patient.html", **data_output)

@mod.route('/make_appointment')
def make_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    doctors = model.get_doctors()
    appointments = model.get_available_appointments()

    data_output = {
        'doctors':doctors,
        'appointments':appointments,
        'content':make_appointment_html
    }

    return render_template("patient.html", **data_output)

@mod.route('/book_appointment', methods=['POST'])
def book_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    patient_id = session['id']
    appointment_id = request.form['appointment_id']
    model.book_appointment(appointment_id, patient_id)

    return redirect(url_for("patient.appointments"))

@mod.route('/unbook_appointment', methods=['POST'])
def unbook_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    appointment_id = request.form['appointment_id']
    model.unbook_appointment(appointment_id)

    return redirect(url_for("patient.appointments"))


@mod.route('/profile')
def profile():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    patient = model.get_patient(session['id'])
    data_output = {
            'patient':patient,
            'content':profile_html
            }

    return render_template("patient.html", **data_output)