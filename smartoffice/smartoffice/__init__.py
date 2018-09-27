#!/usr/bin/env python3
from flask import Flask, session, render_template, redirect, request, url_for, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, DateTimeField
from wtforms_components import DateRange, Email
from datetime import datetime, date
from flask_bootstrap import Bootstrap
import sys
# sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')
sys.path.insert(0,'/Users/User/Downloads/smartoffice/smartofficeA2/smartoffice/smartoffice')
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

import api_caller

from smartoffice.doctor.app import mod
from smartoffice.patient.app import mod
from smartoffice.clerk.app import mod

app.register_blueprint(doctor.app.mod, url_prefix = "/doctor")
app.register_blueprint(patient.app.mod, url_prefix = "/patient")
app.register_blueprint(clerk.app.mod, url_prefix = "/clerk")


bootstrap = Bootstrap(app)

login_html = "login.html"
register_user_html = "register_user.html"
register_doctor_html = "register_doctor.html"
register_clerk_html = "register_clerk.html"
profile_html = "profile.html"


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required(), validators.Length(min=4)])
    phone = TextField('Phone:', validators=[validators.required(), validators.Length(min=10, max=10)])
    birthday  = DateTimeField('Birthday:', format='%Y-%m-%d', validators=[DateRange(min=datetime(1910, 1, 1),max=datetime(2018, 10, 10)), validators.required()])
    email = TextField('Email:', validators=[validators.required(), Email()])

class ReusableFormDoctor(Form):
    name = TextField('Name:', validators=[validators.required(), validators.Length(min=4)])
    email = TextField('Email address', [validators.required(), Email()])
    major = TextField('Major:', validators=[validators.required()])

class ReusableFormClerk(Form):
    name = TextField('Name:', validators=[validators.required(), validators.Length(min=4)])
    email = TextField('Email address', [validators.required(), Email()])

def loginState():
    if 'type' in session:
        if session['type'] == "Doctor":
            return url_for('doctor.availabilities')
        elif session['type'] == "Patient":
            return url_for('patient.appointments')
        elif session['type'] == "MClerk":
            return url_for('clerk.clerkdashboard')
    else: 
        return None

@app.route("/", methods=['GET'])
@app.route("/login")
def login():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    all_patients = api_caller.get_patients()
    all_doctors = api_caller.get_doctors()
    all_clerks = api_caller.get_clerks()
    data_output = {
            'patients':all_patients,
            'doctors':all_doctors,
            'clerks':all_clerks,
            'content':login_html
            }
    return render_template("home.html", **data_output)

@app.route("/login", methods=['POST'])
def loginAction():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    if request.method == 'POST':
        type = request.form['type']
        session['type'] = request.form['type']
        if type == "Doctor":
            session['id'] = request.form['doctor_name']
            return redirect(url_for('doctor.availabilities'))
        elif type == "Patient":
            session['id'] = request.form['patient_name']
            return redirect(url_for('patient.appointments'))
        elif type == "Clerk":
            session['id'] = request.form['clerk_name']
            return redirect(url_for('clerk.clerkdashboard'))


@app.route("/register_patient")
def registerPatient():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    return render_template("home.html", content = register_user_html)

@app.route("/register_patient", methods=['POST'])
def registerPatientAction():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    form = ReusableForm(request.form)
 
    print (form.errors)
    if form.validate() :
        patient_name=request.form['name']
        patient_phone=request.form['phone']
        patient_birthday=request.form['birthday']
        patient_email=request.form['email']
        print (patient_name, " ", patient_phone, " ", patient_birthday, " ", patient_email, " ")
        api_caller.add_patient(patient_name, patient_phone, patient_birthday, patient_email)
        flash('Thanks for registration as a patient, ' + patient_name)
        return redirect('login')
    else:
        flash('Error: Please try again ')
        return redirect('register_patient')
        
 
    # redirect_link = loginState()
    # if redirect_link != None:
    #     return redirect(redirect_link)
    # patient_name = request.form['name']
    # patient_email = request.form['email']           
    # model.add_patient(patient_name,patient_email)
    # return redirect(url_for('login'))

@app.route("/register_doctor")
def registerDoctor():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    return render_template("home.html", content = register_doctor_html)

@app.route("/register_doctor", methods=['POST'])
def registerDoctorAction():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    form = ReusableFormDoctor(request.form)
 
    print (form.errors)
    if form.validate() :
        doctor_name=request.form['name']
        doctor_email=request.form['email']
        doctor_major=request.form['major']
        print (doctor_name, " ", doctor_email, " ", doctor_major, " ")
        api_caller.add_doctor(doctor_name, doctor_email, doctor_major)
        flash('Thanks for registration as a doctor, ' + doctor_name)
        return redirect('login')
    else:
        flash('Error: Please try again ')
        return redirect('register_doctor')
 
@app.route("/register_clerk")
def registerClerk():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    
    return render_template("home.html", content = register_clerk_html)

@app.route("/register_clerk", methods=['POST'])
def registerClerkAction():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)

    form = ReusableFormClerk(request.form)
 
    print (form.errors)
    if form.validate() :
        clerk_name=request.form['name']
        clerk_email=request.form['email']
        print (clerk_name, " ", clerk_email, " ")
        api_caller.add_clerk(clerk_name, clerk_email)
        flash('Thanks for registration as a clerk, ' + clerk_name)
        return redirect('login')
    else:
        flash('Error: Please try again ')
        return redirect('register_clerk')
       
    # doctor_name = request.form['name']
    # doctor_email = request.form['email']
    # doctor_major = request.form['major']
    # model.add_doctor(doctor_name,doctor_major, doctor_email)
    # return redirect(url_for('login'))

@app.route("/patient_record", methods=['POST'])
def patientRecord():
    patient_id = request.form['patient_id']    
    patient = api_caller.get_patient(patient_id)
    data_output = {
            'patient':patient,
            'content':profile_html
            }

    return render_template("patient.html", **data_output)

@app.route('/logout')
def logout():
    session.pop('id',None)
    session.pop('type',None)
    return redirect(url_for('login'))
            
