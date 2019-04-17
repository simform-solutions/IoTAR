import sys
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT
import urllib2
    
 # Get temperature and humidity data from dht11 sensor   
def getSensorData():
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)
    # return dict
    return (str(RH), str(T))
    
# main() function
def main():
    if len(sys.argv) < 2:
        print('Usage: python tstest.py PRIVATE_KEY')
        exit(0)
    print 'starting...'
# url of thingspeak cloud
    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]
   
    while True:
        try:
            RH, T = getSensorData()
            #send data over thingspeak cloud
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s" % (T,RH))
            print f.read()
            f.close()
            sleep(15)
        except:
            print 'exiting.'
            break

# call main
if __name__ == '__main__':
    main()


#run this file
# python dht11.py <api key>
