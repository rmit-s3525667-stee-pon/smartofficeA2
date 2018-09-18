from flask import Blueprint
from flask import Flask,session, render_template, url_for, redirect

mod = Blueprint('patient',__name__,  template_folder='templates')
make_appointment_html = "book_appointment.html"
appointments_html = "appointments.html"

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

    return render_template("patient.html", content = make_appointment_html)

@mod.route('/appointments')
def appointments():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    return render_template("patient.html", content = appointments_html)