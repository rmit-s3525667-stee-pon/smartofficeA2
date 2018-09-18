from flask import Blueprint
from flask import Flask, render_template, session, url_for, redirect

mod = Blueprint('doctor',__name__, template_folder='templates')

def loginState():
    if 'type' in session:
        if session['type'] != "Doctor":
            return url_for('login')
        else:
            return None
    else: 
        return url_for('login')

@mod.route('/')
def doctor():
    redirect_link = loginState()
    if redirect_link != None:
        return redirect(redirect_link)
        
    return render_template('doctor_nav.html')
