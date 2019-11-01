import RPi.GPIO as GPIO
from time import sleep, time
from Tkinter import *
import math

#constats
HEIGHT = 600
WIDTH = 800
SETTLE_TIME = 2             # seconds to let the sensor settle
CALIBRATIONS = 5            # number of calibration measurements to take
CALIBRATION_DELAY = 1       # seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001      # seconds needed to trigger the sensor (to get a measurement)
SPEED_OF_SOUND = 343        # speed of sound in m/s
ROTATION_ANGLE = 15
CANVAS_X_OFFSET = 315
CANVAS_Y_OFFSET = 215
DEBUG = True

# empty lists and variables
ptRadius = 1
distances = []
angles = []
points = []
rotation_counter = 0
correction_factor = 0
angle = 0
scale = 4

#set the RPi to the Broadcom pin layout
GPIO.setmode(GPIO.BCM)
#GPIO pins
TRIG = 18      # the sensor's TRIG pin
ECHO = 27      # the sensor's ECHO pin
GPIO.setup(TRIG, GPIO.OUT)      # TRIG is an output
GPIO.setup(ECHO, GPIO.IN)       # ECHO is an input

class Point(object):
    #constructor
    def __init__(self, distance, angle):
        distance *= scale
        self.xcoord = distance * (math.cos(math.radians(angle)))
        self.ycoord = distance * (math.sin(math.radians(angle)))
    
    #mutator for x-coordinate
    @property
    def xcoord(self):
        return self._xcoord
    
    #setter for x-coordinate    
    @xcoord.setter
    def xcoord(self, xcoord):
        self._xcoord = xcoord
    
    #mutator for y-coordinate
    @property
    def ycoord(self):
        return self._ycoord
    
    #setter for y-coordinate
    @ycoord.setter
    def ycoord(self, ycoord):
        self._ycoord = ycoord

    #magic print function
    def __str__(self):
        return "({},{})".format(float(self.xcoord), float(self.ycoord))
        
def plotPoint(pt):
    grid.create_oval((pt.xcoord + CANVAS_X_OFFSET), \
                     (pt.ycoord + CANVAS_Y_OFFSET), \
                     (pt.xcoord + CANVAS_X_OFFSET) + ptRadius * 2, \
                     (pt.ycoord + CANVAS_Y_OFFSET) + ptRadius * 2, \
                     fill="black", \
                     outline = "black")

def plotPoints(points):
  for i in range(len(points)):
    plotPoint(points[i])

def calibrate():
    global correction_factor
    sleep(SETTLE_TIME)
    known_distance = input("-What is the measured distance (cm)? ")
    distance_avg = 0
    for i in range(CALIBRATIONS) :
        distance= getDistance()
        if (DEBUG):
            print "--Got {}cm".format(distance)
        #  keep a running sum
        distance_avg += distance
        # delay a short time before using the sensor again
        sleep(CALIBRATION_DELAY)
    # calculate the average of the distances
    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print "--Average is {}cm".format(distance_avg)
    #calculate the correction factor
    correction_factor = known_distance / distance_avg
    #if (DEBUG):
        #print "--Correction factor is {}".format(correction_factor)
    print "Done"
    print

# uses the sensor to calculate the distance to an object
def getDistance():
    #######
    # FIX #
    #######
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)      # TRIG is an output
    GPIO.setup(ECHO, GPIO.IN)       # ECHO is an input

    # trigger the sensor by seting it high for a short time and then setting it low
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)
    # wait for the echo pin to read high
    # once the ECHO pin is high, the start time is set
    # once the ECHO pin is low again, the end time is set
    while (GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while (GPIO.input(ECHO) == GPIO.HIGH):
        end = time()
    # calcuate the duration that the ECHO pin was high
    # this is how long the pulse took to get from the sensor to the object -- and back again
    duration = end - start
    # calculate the total distance that the pulse traveled by factoring in the speed of sound (m/s)
    distance = duration * SPEED_OF_SOUND
    # the distance from the sensor is half of the total distance traveled
    distance /= 2
    # convert from meters to centimeters
    distance *= 100
    #distance *= scale
    return distance

def spin():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    
    p = GPIO.PWM(16,50)
    p.start(7.5)
    sleep(.25)
    distances.append(getDistance())
    p.stop()
    GPIO.cleanup()

def echo():
  rotation_counter = 0
  for i in range(0, 360/ROTATION_ANGLE):
    if (stop_button()):
      break
    distance = getDistance() * correction_factor
    angle = ROTATION_ANGLE * rotation_counter
    points.append(Point(distance, angle))
    spin()
    rotation_counter += 1
    #plotPoint(points[i])
    #plotPoints(points)
  plotPoints(points)
  for i in range(1, len(points)):
      grid.create_line(points[i-1].xcoord + CANVAS_X_OFFSET, \
                points[i-1].ycoord + CANVAS_Y_OFFSET, \
                points[i].xcoord + CANVAS_X_OFFSET, \
                points[i].ycoord + CANVAS_Y_OFFSET, fill="black")
  grid.create_line(points[0].xcoord + CANVAS_X_OFFSET, \
                points[0].ycoord + CANVAS_Y_OFFSET, \
                points[-1].xcoord + CANVAS_X_OFFSET, \
                points[-1].ycoord + CANVAS_Y_OFFSET, fill="black")
        
        
def start_button():
    echo()
    #print correction_factor
    
def calibrate_button():
    correction_factor = calibrate()
    
def stop_button():
    pass

sonar = Tk()
lFrame = Frame(sonar, bg = "white", height = HEIGHT, width = WIDTH - 200)
lFrame.pack(side = LEFT)
rFrame = Frame(sonar, bg = "white", height = HEIGHT, width = 200)
rFrame.pack(side = RIGHT)
grid = Canvas(lFrame, bg = "white", height = "600", width = "600")
grid.pack()
calButton = Button(rFrame, command = calibrate_button, text = "Calibrate", bg = "blue", height = "13", width = "27")
calButton.pack(fill = BOTH)
startButton = Button(rFrame, command = start_button, text = "Start", bg = "green", height = "13", width = "27")
startButton.pack(fill = BOTH)
stopButton = Button(rFrame, command = stop_button, text = "Stop", bg = "red", height = "12", width = "27")
stopButton.pack(fill = BOTH)
sonar.title("Sonar Sonic Sensor")


sonar.mainloop()
