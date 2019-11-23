from flask import Flask, render_template
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import numpy as np
import time
import cv2
import os
import argparse
import psycopg2
from psycopg2 import Error

from detection.Detection import yoloDetection

app = Flask(__name__)

app.config['SECRET_KEY'] ='VISON'

def establish_connection():
	try:
	    connection = psycopg2.connect(user = "postgres",
	                                  password = "Ayush3186",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "vison_demo_indexdb")
	    cursor = connection.cursor()
	    # Print PostgreSQL Connection properties
	    print (connection.get_dsn_parameters(),"\n")
	    # Print PostgreSQL version
	    cursor.execute("SELECT version();")
	    record = cursor.fetchone()
	    print("You are connected to - ", record,"\n")
	    return connection

	except (Exception, psycopg2.Error) as error :
	    print ("Error while connecting to PostgreSQL", error)

def close_connection(connection):
	if(connection):
		connection.cursor().close()
		connection.close()
		print("PostgreSQL connection is closed")


def search_table(connection, search_query):
	print("May search")
	try:
		cursor = connection.cursor()
		select_query = "SELECT image_url from image_index where {0} is not null".format(search_query)
		cursor.execute(select_query)
		results = cursor.fetchall()
  
		print("[INFO] Search query successfully")
		return results

	except (Exception, psycopg2.DatabaseError) as error :
	    print ("Error while creating PostgreSQL table", error)

class MyForm(FlaskForm):
    name = StringField('Search: ', validators=[DataRequired()])

@app.route('/')
def index():
	form = MyForm()
	return render_template('home.html', form=form)

@app.route('/', methods=('GET', 'POST'))
def submit():
	form = MyForm()
	if form.validate_on_submit():
		connection = establish_connection()
		search_query = form.name.data
		print(search_query)
		results = search_table(connection, search_query)
		print(results)
		close_connection(connection)
	return render_template('home.html', form=form, results=results)



if __name__ == '__main__':

	ap = argparse.ArgumentParser()
	ap.add_argument("-y", "--yolo", required=True,
		help="base path to YOLO directory")
	ap.add_argument("-i", "--input", required=False,
		help="path to input video")
	ap.add_argument("-c", "--confidence", type=float, default=0.5,
		help="minimum probability to filter weak detections")
	ap.add_argument("-t", "--threshold", type=float, default=0.3,
		help="threshold when applyong non-maxima suppression")
	ap.add_argument("-b", "--bbox", required=False, default=True,
		help="turn on bounding box")
	args = vars(ap.parse_args())

	detector = yoloDetection(args["yolo"], args["input"], args["confidence"],
		args["threshold"], args["bbox"])

	detector.prepareModel('search_detection')
    
    #SSD_NET
    if input("Want to get SSD_NET for video ?(Y/N): ") in {'Y', 'y'}:         #needs to be automated by some instance
        parser = argparse.ArgumentParser(description='Script to run MobileNet-SSD object detection network ')
        parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
        parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",help='Path to text network file: MobileNetSSD_deploy.prototxt for Caffe model or ')
        parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",help='Path to weights: MobileNetSSD_deploy.caffemodel for Caffe model or ')
        parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
        args = parser.parse_args()
        
        classNames = { 0: 'background', 1: 'airplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair', 10: 'cow', 11: 'dining table', 12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person', 16: 'potted plant', 17: 'sheep', 18: 'couch', 19: 'train', 20: 'tvmonitor' }
        # the className must be extended in case of addition of new data for new classes. all these classes are already a part of the coco with aliases for a few
        
        #for video input
        if args.video:            cap = cv2.VideoCapture(args.video)
        else:            cap = cv2.VideoCapture(0)
            
        net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)     #
        
        while 1:        #infinite loop
            #framing the relevant image
            ret, frame = cap.read()
            frame_resized = cv2.resize(frame,(300,300)) 
            blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
            net.setInput(blob)
            detections = net.forward()
            
            cols = frame_resized.shape[1] 
            rows = frame_resized.shape[0]

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > args.thr: 
                    class_id = int(detections[0, 0, i, 1]) 
                    xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                    yLeftBottom = int(detections[0, 0, i, 4] * rows)
                    xRightTop   = int(detections[0, 0, i, 5] * cols)
                    yRightTop   = int(detections[0, 0, i, 6] * rows)
                    # scaling the object
                    heightFactor = frame.shape[0]/300.0  
                    widthFactor = frame.shape[1]/300.0 

                    xLeftBottom = int(widthFactor * xLeftBottom) 
                    yLeftBottom = int(heightFactor * yLeftBottom)
                    xRightTop   = int(widthFactor * xRightTop)
                    yRightTop   = int(heightFactor * yRightTop)
  
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                                  (0, 255, 0))

                    if class_id in classNames:
                        label = classNames[class_id] + ": " + str(confidence)
                        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                        yLeftBottom = max(yLeftBottom, labelSize[1])
                        cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                             (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                             (255, 255, 255), cv2.FILLED)
                        cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                        print label
                        
            cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) >= 0:
                break
    
    
    
    #For images
    
    if input("Want to get SSD_NET for image ?(Y/N): ") in {'Y', 'y'}:
        parser = argparse.ArgumentParser(description='Script to run MobileNet-SSD object detection network')
        parser.add_argument("--image", default= "img.jpeg", help="path to video file. If empty, camera's stream will be used")
        parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt", help='Path to text network file: MobileNetSSD_deploy.prototxt for Caffe model'}
        parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel", help='Path to weights: MobileNetSSD_deploy.caffemodel for Caffe model' )
        parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
        args = parser.parse_args()

        # Labels of Network.
        classNames = { 0: 'background', 1: 'airplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair', 10: 'cow', 11: 'dining table', 12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person', 16: 'potted plant', 17: 'sheep', 18: 'couch', 19: 'train', 20: 'tvmonitor' }

        #Load the Caffe model 
        net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

        frame = cv2.imread(args.image)
        frame_resized = cv2.resize(frame,(300,300)) 
        heightFactor = frame.shape[0]/300.0
        widthFactor = frame.shape[1]/300.0 
        
        # shape be (1, 3, 300, 300)
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        net.setInput(blob)
        detections = net.forward()

        frame_copy = frame.copy()
        frame_copy2 = frame.copy()
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]
 .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  
            if confidence > args.thr:  
                class_id = int(detections[0, 0, i, 1]) 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)

                xLeftBottom_ = int(widthFactor * xLeftBottom) 
                yLeftBottom_ = int(heightFactor* yLeftBottom)
                xRightTop_   = int(widthFactor * xRightTop)
                yRightTop_   = int(heightFactor * yRightTop)
                cv2.rectangle(frame_resized, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                              (0, 255, 0))

                cv2.rectangle(frame_copy, (xLeftBottom_, yLeftBottom_), (xRightTop_, yRightTop_),
                              (0, 255, 0),-1)
        opacity = 0.3
        cv2.addWeighted(frame_copy, opacity, frame, 1 - opacity, 0, frame)

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  
            if confidence > args.thr: 
                class_id = int(detections[0, 0, i, 1]) 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)

                xLeftBottom_ = int(widthFactor * xLeftBottom) 
                yLeftBottom_ = int(heightFactor* yLeftBottom)
                xRightTop_   = int(widthFactor * xRightTop)
                yRightTop_   = int(heightFactor * yRightTop)
                cv2.rectangle(frame, (xLeftBottom_, yLeftBottom_), (xRightTop_, yRightTop_),
                  (0, 0, 0),2)
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_TRIPLEX, 0.8, 1)

                    yLeftBottom_ = max(yLeftBottom_, labelSize[1])
                    cv2.rectangle(frame, (xLeftBottom_, yLeftBottom_ - labelSize[1]),
                                         (xLeftBottom_ + labelSize[0], yLeftBottom_ + baseLine),
                                         (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom_, yLeftBottom_),
                                cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 0, 0))
                    print label  
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow("frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    app.run(debug=True)