from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
import time
import sys
sys.path.insert(0,'/home/pi/playground/smartofficeA2/smartoffice-crud/smartoffice')
mod = Blueprint('doctor',__name__, template_folder='templates')

from smartoffice import model

# Add a Doctor to the system
@mod.route('',methods=['POST'])
def add_doctor():
    name = request.json['name']
    email = request.json['email']
    major = request.json['major']
    new_doctor = model.add_doctor(name, email, major)
    return model.doctor_schema.jsonify(new_doctor)

# Get All Doctor
@mod.route('',methods=['GET'])
def get_doctors():
    doctors = model.get_doctors()
    return model.doctors_schema.jsonify(doctors)

# Get Doctor by Id
@mod.route('/<id>', methods=['GET'])
def get_doctor(id):
    doctor = model.get_doctor(id)
    return model.doctor_schema.jsonify(doctor)