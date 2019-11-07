import RPi.GPIO as GPIO
from time import sleep, time
from Tkinter import *
import math

HEIGHT = 600                # height omf the window
WIDTH = 800                 # width of the window
SETTLE_TIME = 2             # seconds to let the sensor settle
CALIBRATIONS = 5            # number of calibration measurements to take
CALIBRATION_DELAY = 1       # seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001      # seconds needed to trigger the sensor (to get a measurement)
SPEED_OF_SOUND = 343        # speed of sound in m/s
ROTATION_ANGLE = 15         # angle the sensor rotates every cycle
CANVAS_X_OFFSET = 315       # centers the x coordinate of the measured point
CANVAS_Y_OFFSET = 215       # centers the y coordinate of the measured point
DEBUG = True
TRIG = 18      # the sensor's TRIG pin
ECHO = 27      # the sensor's ECHO pin
SERVO = 16

ptRadius = 1                # radius of the plotted point
distances = []              # list of measured distances
points = []                 # list of calculated points to plot
rotation_counter = 0        # counter of measurement cycles
correction_factor = 0       # correction factor of USS
angle = 0                   # initializes value of angle to be assigned later
scale = 4                   # functions as a zoom in order to make the plotted points and shape more visible
global_stop = False         # stop globally

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)      # TRIG is an output
GPIO.setup(ECHO, GPIO.IN)       # ECHO is an input
GPIO.setup(SERVO, GPIO.OUT)

class Point(object):
    #constructor
    def __init__(self, distance, angle):
        distance *= scale   # increases magnitude by scale factor
        self.xcoord = distance * (math.cos(math.radians(angle)))    # calculates x coordinate from given polar coordinates
        self.ycoord = distance * (math.sin(math.radians(angle)))    # calculates y coordinate from given polar coordinates
    
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

def plotPoint(pt):      # function that plots the calculated points to the canvas
    grid.create_oval((pt.xcoord + CANVAS_X_OFFSET), \
                     (pt.ycoord + CANVAS_Y_OFFSET), \
                     (pt.xcoord + CANVAS_X_OFFSET) + ptRadius * 2, \
                     (pt.ycoord + CANVAS_Y_OFFSET) + ptRadius * 2, \
                     fill="black", \
                     outline = "black")

def plotPoints(points): # calls plotPoint function for every point in list points
  for i in range(len(points)):
    plotPoint(points[i])
    
def calibrate():                    # calibrates the USS in order to gather accurate distance data
    global correction_factor        # allows correction_factor to be modified in the local scope
    sleep(SETTLE_TIME)              # allows sensor to "settle"
    known_distance = 20
    distance_avg = 0
    for i in range(CALIBRATIONS) :  # gathers series of distances in order to calulate variance
        distance = getDistance()
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
    
def getDistance():                  # uses the sensor to calculate the distance to an object
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

def spin():                 # tells the servo to spin
    p = GPIO.PWM(SERVO,50)     # assigns GPIO output of pins for servo
    # creates duty cycle for the servo
    p.start(7.5)
    sleep(.0435)
    # measures distance
    distances.append(getDistance()) ##maybe not needed?? ##
    p.stop()
    #GPIO.cleanup()

def echo():
  rotation_counter = 0 ## maybe not needed?? ##
  # executes i times in order to create a closed shape
  for i in range(0, 360/ROTATION_ANGLE):
    if (global_stop == True):
      points.clear()
      break
    distance = getDistance() * correction_factor        # calculates accurate distance
    angle = ROTATION_ANGLE * rotation_counter           # calculates accurate angle
    points.append(Point(distance, angle))               # calculates point to plot
    spin()                                              # spins servo
    rotation_counter += 1                               # increments counter
  plotPoints(points)
  for i in range(1, len(points)):                       # creates line from each point to the next in list points
    if (global_stop == True):
      break
    grid.create_line(points[i-1].xcoord + CANVAS_X_OFFSET, \
                points[i-1].ycoord + CANVAS_Y_OFFSET, \
                points[i].xcoord + CANVAS_X_OFFSET, \
                points[i].ycoord + CANVAS_Y_OFFSET, fill="black")
  if (global_stop == False):
    grid.create_line(points[0].xcoord + CANVAS_X_OFFSET, \
                points[0].ycoord + CANVAS_Y_OFFSET, \
                points[-1].xcoord + CANVAS_X_OFFSET, \
                points[-1].ycoord + CANVAS_Y_OFFSET, fill="black")
        
        
def start_button():                                     # assigns functionality of start button
    echo()
    
def calibrate_button():                                 # assigns functionality of calibrate button
    correction_factor = calibrate()
    
def stop_button():                                      # # assigns functionality of stop button ##
    global_stop = True

# creates the instance of the GUIK
sonar = Tk()
# creates frame for left side of the GUI
lFrame = Frame(sonar, bg = "white", height = HEIGHT, width = WIDTH - 200)
lFrame.pack(side = LEFT)
# creates frame for right side of the GUI
rFrame = Frame(sonar, bg = "white", height = HEIGHT, width = 200)
rFrame.pack(side = RIGHT)
# creates cnavas to plot points to
grid = Canvas(lFrame, bg = "white", height = "600", width = "600")
grid.pack()
# creates calibrate button
calButton = Button(rFrame, command = calibrate_button, text = "Calibrate", bg = "blue", height = "13", width = "27")
calButton.pack(fill = BOTH)
# creates start button
startButton = Button(rFrame, command = start_button, text = "Start", bg = "green", height = "13", width = "27")
startButton.pack(fill = BOTH)
# creates stop button
stopButton = Button(rFrame, command = stop_button, text = "Stop", bg = "red", height = "12", width = "27")
stopButton.pack(fill = BOTH)
# set name of the window
sonar.title("Sonar Sonic Sensor")

# runs the GUI
sonar.mainloop()
