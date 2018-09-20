from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
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
    doctors = model.get_doctors()
    for doctor in doctors:
        print(doctor.name)
    return render_template('doctor_nav.html', content = appointments_html)

@mod.route('/appointments', methods=['POST'])
def add_appointments():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    start = request.form['start']
    end = request.form['end']
    print(start)
    print(end)
    return redirect(url_for('doctor.doctor'))
