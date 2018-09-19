#!/usr/bin/env python3
from flask import Flask, session, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

USER = 'root'
PASS = 'oliverwood98'
HOST = '35.197.183.53'
DBNAME = 'smartoffice'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('name','email')
    
user_schema = PatientSchema()
users_schema = PatientSchema(many = True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    major = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, major, email):
        self.name = name
        self.major = major
        self.email = email

class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('name','major','email')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many = True)

def add_patient(name, email):
    new_patient = Patient(name,email)
    db.session.add(new_patient)
    db.session.commit()

def get_patients():
    all_patients = Patient.query.all()
    return all_patients

def add_doctor(name, email, major):
    new_doctor = Doctor(name,email,major)
    db.session.add(new_doctor)
    db.session.commit()

def get_doctors():
    all_doctors = Doctor.query.all()
    return all_doctors


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
    all_patients = get_patients()
    all_doctors = get_doctors()
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
            return redirect(url_for('doctor.doctor'))
        elif type == "Patient":
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
    add_patient(patient_name,patient_email)
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
    add_doctor(doctor_name,doctor_major, doctor_email)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('type',None)
    return redirect(url_for('login'))
            
