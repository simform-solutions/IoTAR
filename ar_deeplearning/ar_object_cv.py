#!/usr/bin/python
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
 
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the camera sensor to warm up,
# and initialize the FPS counter
print("[INFO] starting video stream...")
#vs = cv2.VideoCapture(0)
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        Percentage = (dist-25.6)/25.6*100
        print("level :"+str(abs(Percentage)))
        frame = vs.read()
        frame = imutils.resize(frame, width=900)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (150, 150)),
                0.007843, (150, 150), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                #print (detections)
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if int(detections[0, 0, i, 1]) == 5: 
                        if confidence > args["confidence"]:
                                # extract the index of the class label from the
                                # `detections`, then compute the (x, y)-coordinates of
                                # the bounding box for the object
                                idx = int(detections[0, 0, i, 1])
                                print(idx)
                                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                (startX, startY, endX, endY) = box.astype("int")
                                '''
                                # draw the prediction on the frame
                                label = "{}: {:.2f}%".format(CLASSES[idx],
                                        confidence * 100)
                                cv2.rectangle(frame, (startX, startY), (endX, endY),
                                        COLORS[idx], 2)
                                y = startY - 15 if startY - 15 > 15 else startY + 15
                                cv2.putText(frame, label, (startX, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                                        '''
                                dist = distance()
                                print ("Measured Distance = %.1f cm" % dist)
                                dis = round(dist, 2)
                                print(dis)
                                Percentage = (dis-25.6)/25.6*100
                                per = round(Percentage, 2)
                                #humidity, temperature = Adafruit_DHT.read_retry(11, 4)
                                #cv2.putText(frame,'Temprature ='+str(temperature), (startX - 250, startY + 300),
                                   # cv2.FONT_HERSHEY_SIMPLEX, 1, (11,255,255), 2, cv2.LINE_AA)

                                #Set water level value on video frame    
                                cv2.putText(frame,'WATER LEVEL ='+str(abs(per))+' %', (startX, startY - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (11,255,255), 2, cv2.LINE_AA)



        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

        # update the FPS counter
        fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()



			
	



