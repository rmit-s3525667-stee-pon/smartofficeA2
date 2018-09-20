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

@mod.route('/appointments')
def doctor():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    all_appointments = model.get_appointments()
    data_output = {
        'appointments':all_appointments,
        'content':lppointments_html
    }

    return render_template('doctor_nav.html', **data_output)

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
 
    model.add_appointment(doctor_id, date, time_start, time_end, patient_id)
    return redirect(url_for("doctor.add_appointments"))
