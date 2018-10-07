#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
sys.path.insert(0,'/home/pi/A2/smartoffice/smartoffice/')

import api_caller

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

current_doctor = -1
patient_id = -1
patient_note = ""

def set_doctor(string):
    global current_doctor
    doctor_name = string[8:len(string)]
    doctor = api_caller.get_doctor_by_name(doctor_name)
    if doctor != None:
        sayHi = "Hi" + doctor_name
        current_doctor = doctor.id
        aiy.audio.say(sayHi)
    else:
        current_doctor = -1
        aiy.audio.say("Sorry but I didn't know you")

def unset_doctor():
    global current_doctor
    global patient_note
    current_doctor = -1
    patient_id = -1
    patient_note = ""
    aiy.audio.say("Goodbye Doctor")

def make_note(string):
    global patient_id
    global patient_note
    patient_name = string[14:len(string)]
    patient = api_caller.get_patient_by_name(patient_name)
    if patient != None:
        patient_id = patient.id
        patient_note = ""
        aiy.audio.say("What do you want to add to the notes, doctor ?")
    else:
        patient_id = -1
        aiy.audio.say("No patient have this name in the system")

def add_note(string):
    global patient_note
    if patient_note == "":
        patient_note = patient_note + string[8:len(string)]
    else:
        patient_note = patient_note + "," + string[14:len(string)]
    aiy.audio.say("Note have been added to notes")

def clear_note():
    global patient_note
    patient_note = ""
    aiy.audio.say("Note have been clear")

def save_note():
    global current_doctor
    global patient_id
    global patient_note
    api_caller.add_medical_record(current_doctor, patient_id, patient_note)
    patient_id = -1
    aiy.audio.say("Notes for patient have been save to the cloud")


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, event):
    print(event)
    global current_doctor
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text[0:7] == "this is":
            assistant.stop_conversation()
            set_doctor(text)
        elif text == "thanks for your help":
            assistant.stop_conversation()
            unset_doctor()
        elif current_doctor != -1 and text[0:13] == "make note for":
            assistant.stop_conversation()
            make_note(text)
        elif current_doctor != -1 and patient_id != -1 and text[0:7] == "patient":
            assistant.stop_conversation()
            add_note(text)
        elif current_doctor != -1 and patient_id != -1 and text[0:9] == "save note":
            assistant.stop_conversation()
            save_note()
        elif current_doctor != -1 and text[0:10] == "clear note":
            assistant.stop_conversation()
            clear_note()

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
