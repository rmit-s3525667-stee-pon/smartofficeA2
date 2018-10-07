# USAGE
# With default parameters
# 		python3 03_recognise.py
# OR specifying the encodings, screen resolution, output video and display
# 		python3 03_recognise.py -e encodings.pickle -r 240 -o output/capture.avi -y 1

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream

import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import requests, json, sys, time, datetime

sys.path.insert(0,'/Users/BramanthaPatra/A2Git/smartofficeA2/smartoffice/smartoffice')
import api_caller

# NEW: gRPC related stuffs

import os
import grpc

import sensehat_led_grpc
import sensehat_led

# Access token for pushbullet (April)
# ACCESS_TOKEN="o.EXTFdjewnfTNmJ4txKuKg6nBGdWZ8VXm"
# Access token for pushbullet (Bram)
ACCESS_TOKEN="o.s4LvqhrQwluDA91nkcrsW9u8XfGXeacA"

URL = 'http://10.132.80.171/'
patient_code = 'patient'
host = 'localhost'
grpc_host = '10.132.80.171'

eye_detector = cv2.CascadeClassifier('haarcascade_eye.xml')

# gRPC to control the pi
def sensehat_led_light(colour):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    with grpc.insecure_channel('{}:50051'.format(grpc_host)) as channel:
        stub = sensehat_led_grpc.GreeterStub(channel)
        response = stub.SayHello(sensehat_led.HelloRequest(name=colour))


# Send notification to user via pushbullet
# Code from tutelab 4 and have been reference and modified for education purpose
def send_notification_via_pushbullet(title, body):
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})

def main():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-e", "--encodings", default='encodings.pickle',
		help="path to serialized db of facial encodings")
	ap.add_argument("-r", "--resolution", type=int, default=240,
	        help="Resolution of the video feed")
	ap.add_argument("-o", "--output", type=str,
		help="path to output video")
	ap.add_argument("-y", "--display", type=int, default=1,
		help="whether or not to display output frame to screen")
	ap.add_argument("-d", "--detection-method", type=str, default="cnn",
		help="face detection model to use: either 'hog' or 'cnn'")
	args = vars(ap.parse_args())

	# load the known faces and embeddings
	print("[INFO] loading encodings...")
	data = pickle.loads(open(args["encodings"], "rb").read())
	# face_data = pickle.loads(open("{}/face".format(args["encodings"]), "rb").read())


	# initialize the video stream and pointer to output video file, then
	# allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	writer = None
	time.sleep(2.0)

	match = 0
	do_not_match = 0
	exist = None

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream
		frame = vs.read()

		# convert the input frame from BGR to RGB then resize it to have
		# a width of 240px (to speedup processing)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		rgb = imutils.resize(frame, width=args["resolution"])
		r = frame.shape[1] / float(rgb.shape[1])

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input frame, then compute
		# the facial embeddings for each face
		boxes = face_recognition.face_locations(rgb,
			model=args["detection_method"])
		encodings = face_recognition.face_encodings(rgb, boxes)
		names = []

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],encoding)
			
			name = ""

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face

				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

				# NEW: loop multiple times to ensure the images are precise
				match += 1 

			else:
				do_not_match += 1

			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# rescale the face coordinates
			top = int(top * r)
			right = int(right * r)
			bottom = int(bottom * r)
			left = int(left * r)

			# draw the predicted face name on the image
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				0.75, (0, 255, 0), 2)

		# if the video writer is None *AND* we are supposed to write
		# the output video to disk initialize the writer
		if writer is None and args["output"] is not None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter(args["output"], fourcc, 20,
				(frame.shape[1], frame.shape[0]), True)

		# if the writer is not None, write the frame with recognized
		# faces to disk
		if writer is not None:
			writer.write(frame)

		# check to see if we are supposed to display the output frame to
		# the screen
		if args["display"] > 0:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

		# NEW: if the patient's face is recognized by the system for 10 times,
		# a pushbullet notification will be sent
		if match == 10:

				patients = api_caller.get_patients()
				patients_dumps = json.dumps(patients, default=lambda o: o.__dict__, sort_keys=True, indent=4)
				patients_loads = json.loads(patients_dumps)

				appointments = api_caller.get_appointments()
				appointments_dumps = json.dumps(appointments, default=lambda o: o.__dict__, sort_keys=True, indent=4)
				appointments_loads = json.loads(appointments_dumps)

				now = datetime.datetime.now()
				n1h = now + datetime.timedelta(hours=1)
				n1w = now + datetime.timedelta(days=7)
				now_date = now.strftime("%Y-%m-%d")
				next_one_week = datetime.datetime.strftime(n1w, '%Y-%m-%d')
				next_one_hour = datetime.datetime.strftime(n1h, '%H:%M:%S')


				
				for patient in patients_loads:
					if patient['name'] ==  name:
						print("Patient exists in database")	
						sensehat_led_light("green")
						exist = True
						for appointment in appointments_loads:
							# print("Patient exists in database")
							if appointment['patient_id'] == patient['id']:
								# print("You have an appointment")
								# if appointment['date'] == next_one_week:
								if appointment['date'] == now_date:
									# print("You have an appointment today next week")
									# st = datetime.datetime.strptime(appointment['time_start'], "%H:%M:%S")
									# if next_one_hour < appointment['time_start']: 
									if appointment['time_start'] < next_one_hour: 
										print("You have an appointment in the next one hour")
										send_notification_via_pushbullet("Patient {} has arrived!".format(name), \
											"Here's a link to the patient's medical record: {}/doctor/medical_record/{}".format(host, patient['id']))
										break
									else:
										print("You don't have any appointment in the next one hour")
										break

				# print("Face is recognized")
				sys.exit()

		elif do_not_match == 10:
			print("Patient does not exist in database")	
			sensehat_led_light("red")
			sys.exit()


				

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

	# check to see if the video writer point needs to be released
	if writer is not None:
		writer.release()




# run()
main()
