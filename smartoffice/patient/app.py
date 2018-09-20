from flask import Blueprint
from flask import Flask,session, render_template, url_for, redirect
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

@mod.route('/make_appointment')
def make_appointment():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    patients = model.get_patients()
    for patient in patients:
        print(patient.name)
    return render_template("patient.html", content = make_appointment_html)

@mod.route('/appointments')
def appointments():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    return render_template("patient.html", content = appointments_html)

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