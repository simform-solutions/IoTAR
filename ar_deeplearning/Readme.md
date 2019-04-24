# Augmented Reality Deep learning object detection with opencv on Raspberrypi


![](demo.gif)

Raspberrypi run deep learning object detection with opencv used for detect bottel object and ultrasonic sensor connected with raspberrypi and it put on top of bottel for measure water level of bottel if bottel detected then water level measured by sensor show up on bottel in video frame using opencv.

For object detection tensorflow pretrained mobilenetssd model used in this project mobilenetssd model able to detect more than 20 object but in project code is set to detect only bottel object.

##Requirements

Hardware

RaspberryPi
Pi cam
Ultrasonic sensor

Software

Opencv (3.4.3)
Python (3)


### Run project

python3 ar_object_cv.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel



