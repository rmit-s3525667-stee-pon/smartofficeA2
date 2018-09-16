from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from httplib2 import Http
from datetime import datetime
from datetime import timedelta
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
 
 
@app.route("/doctor", methods=['GET'])
def patient():
    form = ReusableForm(request.form)

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
 
    # print(form.errors)
    # if request.method == 'POST':
    #     name=request.form['name']
    #     password=request.form['password']
    #     email=request.form['email']
    #     print(name, " ", email, " ", password)
 
    #     if form.validate():
    #         # Save the comment here.
    #         flash('Thanks for registration ' + name)
    #     else:
    #         flash('Error: All the form fields are required. ')
 
    return render_template('doctor.html', events=events)


# RMIT wireless network
if __name__ == "__main__":
	host = os.popen('hostname -I').read()
	app.run(host=host, port=80, debug=False)
	
"""
For home wireless

if __name__ == '__main__':
    app.run(host='0.0.0.0')

"""
