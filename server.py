import os
import numpy as np
import argparse
import cv2

from flask import Flask, render_template, Response, jsonify, request, send_file, send_from_directory
from pprint import pprint
from werkzeug.utils import secure_filename
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filters import threshold_adaptive

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def transform_file(file):
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED) # make img from request to np array
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    print ("STEP 1: Edge Detection")
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    # loop over the contours
    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    	# if our approximated contour has four points, then we
    	# can assume that we have found our screen
    	if len(approx) == 4:
    		screenCnt = approx
    		break

    print ("STEP 2: Find contours of paper")
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    warped = threshold_adaptive(warped, 251, offset = 10)
    warped = warped.astype("uint8") * 255
    # would be nicer to leave the writing to another function? not sure
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), warped)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST'])
def index():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        warped = transform_file(file)
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
