from flask import Blueprint
from flask import Flask, request, jsonify
import sys
sys.path.insert(0,'/home/pi/playground/smartofficeA2/smartoffice-crud/smartoffice')
mod = Blueprint('patient',__name__,  template_folder='templates')

from smartoffice import model

# Add a Patient to the system
@mod.route('',methods=['POST'])
def add_patient():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    birthday = request.json['birthday']
    new_patient = model.add_patient(name, phone, birthday, email)
    return model.patient_schema.jsonify(new_patient)

# Get a Patient 
@mod.route('/<id>', methods=['GET'])
def get_patient(id):
    patient = model.get_patient(id)
    return model.patient_schema.jsonify(patient)

# Get all Patient
@mod.route('',methods=['GET'])
def get_patients():
    patients = model.get_patients()
    return model.patients_schema.jsonify(patients)



