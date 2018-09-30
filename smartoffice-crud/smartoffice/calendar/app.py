from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request

import time
import sys

# Minh's pi
# sys.path.insert(0,'/home/pi/playground/smartofficeA2/smartoffice-crud/smartoffice')
# Bram and April's pi
sys.path.insert(0,'/home/pi/A2/smartoffice-crud/smartoffice')

mod = Blueprint('calendar',__name__, template_folder='templates')

from smartoffice import model


@mod.route('/<id>', methods=['DELETE'])
def remove_from_calendar(id):
    model.remove_from_calendar(id)
    return "Deleted"

@mod.route('', methods=['POST'])
def add_to_calendar():
    summary = request.json['summary']
    doctor_id = request.json['doctor_id']
    date = request.json['date']
    time_start = request.json['time_start']
    time_end = request.json['time_end']
    calendar_id = request.json['calendar_id']
    model.add_to_calendar(summary, doctor_id, date, time_start, time_end, calendar_id)
    return "Added"
