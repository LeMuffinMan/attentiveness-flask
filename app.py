import sys
from sys import stdout
from process import webopencv
import logging
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64
import random
from time import sleep



#----------------- Video Transmission ------------------------------#
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['DEBUG'] = True
socketio = SocketIO(app)
camera = Camera(webopencv())

#---------------- Video Transmission --------------------------------#


#---------------- Video Socket Connections --------------------------#
@socketio.on('input image', namespace='/test')
def test_message(input):
	input = input.split(",")[1]
	camera.enqueue_input([input, (request.sid)])
	sleep(0.2)


@socketio.on('connect', namespace='/test')
def test_connect():
	app.logger.info("client connected")
	userID = request.sid
	print(str(userID)+ " CONNECTED --------------------")
	sys.stdout.flush()

@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')


def gen(userID):
	"""Video streaming generator function."""

	app.logger.info("starting to generate frames!")
	while True:
		frame = camera.get_frame(userID) 
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		
@app.route('/', defaults={'userID': ''})
@app.route('/video_feed/<userID>')
def video_feed(userID):
	"""Video streaming route. Put this in the src attribute of an img tag."""
	return Response(gen(userID), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	socketio.run(app)
