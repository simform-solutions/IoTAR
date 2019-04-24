import sys
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT
import urllib2
import requests

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
    
    
# main() function
def main():

    def read_data_thingsboard():
     #Thingsboard url
        NEW_URL="https://demo.thingsboard.io/api/v1/wMQkmvzyasQ6MoeUMpLH/attributes"
        print(NEW_URL)
     #Get json from thingsboard
        get_data=requests.get(NEW_URL).json()
        print(get_data)
        channel_id = get_data['client']['key1']
        #print channel_id
        if channel_id == 100:
                GPIO.output(8, GPIO.HIGH) # Turn on
                
        else:
                GPIO.output(8, GPIO.LOW) # Turn off   
    while True:
            read_data_thingsboard()
            #sleep(1)
        

# call main
if __name__ == '__main__':
    main()
