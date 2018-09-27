from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect, request
import time
import sys
sys.path.insert(0,'/home/pi/A2/smartoffice-crud/smartoffice')
mod = Blueprint('clerk',__name__, template_folder='templates')

from smartoffice import model

# Add a Clerk to the system
@mod.route('',methods=['POST'])
def add_clerk():
    name = request.json['name']
    email = request.json['email']
    new_clerk = model.add_clerk(name, email)
    return model.clerk_schema.jsonify(new_clerk)

# Get All Clerk
@mod.route('',methods=['GET'])
def get_clerks():
    clerks = model.get_clerks()
    return model.clerks_schema.jsonify(clerks)

# Get Clerk by Id
@mod.route('/<id>', methods=['GET'])
def get_clerk(id):
    clerk = model.get_clerk(id)
    return model.clerk_schema.jsonify(clerk)