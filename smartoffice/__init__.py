#!/usr/bin/env python3
from flask import Flask, session, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')

import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

USER = 'root'
PASS = 'password'
HOST = '35.201.22.140'
DBNAME = 'smartoffice-db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

import model

from smartoffice.doctor.app import mod
from smartoffice.patient.app import mod

app.register_blueprint(doctor.app.mod, url_prefix = "/doctor")
app.register_blueprint(patient.app.mod, url_prefix = "/patient")

bootstrap = Bootstrap(app)

login_html = "login.html"
register_user_html = "register_user.html"
register_doctor_html = "register_doctor.html"

def loginState():
    if 'type' in session:
        if session['type'] == "Doctor":
            return url_for('doctor.doctor')
        elif session['type'] == "Patient":
            return url_for('patient.appointments')
    else: 
        return None

@app.route("/", methods=['GET'])
@app.route("/login")
def login():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
    all_patients = model.get_patients()
    all_doctors = model.get_doctors()
    data_output = {
            'patients':all_patients,
            'doctors':all_doctors,
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
            return redirect(url_for('doctor.doctor'))
        elif type == "Patient":
            session['id'] = request.form['patient_name']
            return redirect(url_for('patient.appointments'))

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
        
    patient_name = request.form['name']
    patient_email = request.form['email']
    model.add_patient(patient_name,patient_email)
    return redirect(url_for('login'))

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
    
    doctor_name = request.form['name']
    doctor_email = request.form['email']
    doctor_major = request.form['major']
    model.add_doctor(doctor_name,doctor_major, doctor_email)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('id',None)
    session.pop('type',None)
    return redirect(url_for('login'))
            
