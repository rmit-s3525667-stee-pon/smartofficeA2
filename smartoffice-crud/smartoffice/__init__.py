#!/usr/bin/env python3
from flask import Flask, session, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sys

#Path to model
sys.path.insert(0,'/home/pi/A2/smartoffice-crud/smartoffice')
sys.path.insert(0,'/home/pi/A2/smartoffice-crud/smartoffice/config/')
import os
import server_config
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

USER = server_config.get_user()
PASS = server_config.get_pass()
HOST = server_config.get_host()
DBNAME = server_config.get_dbname()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

import model

from smartoffice.doctor.app import mod
from smartoffice.patient.app import mod
from smartoffice.clerk.app import mod
from smartoffice.appointment.app import mod
from smartoffice.availability.app import mod
from smartoffice.calendar.app import mod

# import all the blueprint app 
app.register_blueprint(doctor.app.mod, url_prefix = "/doctor")
app.register_blueprint(patient.app.mod, url_prefix = "/patient")
app.register_blueprint(clerk.app.mod, url_prefix = "/clerk")
app.register_blueprint(appointment.app.mod, url_prefix = "/appointment")
app.register_blueprint(availability.app.mod, url_prefix = "/availability")
app.register_blueprint(calendar.app.mod, url_prefix = "/calendar")

