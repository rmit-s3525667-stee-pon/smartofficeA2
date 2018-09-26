from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request

import time
import sys
sys.path.insert(0,'/home/pi/playground/smartofficeA2/smartoffice-crud/smartoffice')
mod = Blueprint('availability',__name__, template_folder='templates')

from smartoffice import model

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

@mod.route('', methods=['POST'])
def add_availability():
    doctor_id = request.json['doctor_id']
    date = request.json['date']
    time_start = request.json['time_start']
    time_end = request.json['time_end']
    event_id = request.json['event_id']
    new_availability = model.add_availability(doctor_id, date, time_start, time_end, event_id)
    return model.availability_schema.jsonify(new_availability)

@mod.route('', methods=['GET'])
def get_availability():
    availabilities = model.get_availability()
    return model.availabilities_schema.dumps(availabilities, default = date_handler )

@mod.route('/doctor/<id>', methods=['GET'])
def get_availability_by_doctor(id):
    availabilities = model.get_availability_by_doctor(id)
    return model.availabilities_schema.dumps(availabilities, default = date_handler )

@mod.route('/<id>', methods=['DELETE'])
def remove_availability(id):
    model.remove_availability(id)
    return "Deleted"
