from math import *
from random import randint

# GUI setup
from Tkinter import *

# the 2D point class
class Point(object):
  def __init__(self, x = 0, y = 0):
    self.x = float(x)
    self.y = float(y)

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, value):
    self._x = value

  @property
  def y(self):
    return self._y

  @y.setter
  def y(self, value):
    self._y = value

  def dist(self, other):
    return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

  def midpt(self, other):
    newX = (self.x + other.x) / 2
    newY = (self.y + other.y) / 2
    return Point(newX, newY)

  def __str__(self):
    return "({},{})".format(self.x, self.y)

# the canvas class
class CoordinateSystem(Canvas):
  ptRadius = 1
  ptColor = "black"
  
  def __init__(self, window):
    Canvas.__init__(self, window, bg="white")
    self.pack(fill = Y, expand = 1)

  def plotPoints(self, points):
    for i in range(len(points)):
      self.plotPoint(points[i])

  def plotPoint(self, pt):
    self.create_oval(pt.x, pt.y, pt.x + \
                     CoordinateSystem.ptRadius * 2, \
                     pt.y + CoordinateSystem.ptRadius * 2, \
                     fill=CoordinateSystem.ptColor, \
                     outline = CoordinateSystem.ptColor)
  
# the sensor class
class Sensor(Frame):
  # the layout
  # O O O C
  # O O O S
  # O O O Q
  
  # the constructor
  def __init__(self, parent):
    # call the constructor in the superclass
    Frame.__init__(self, parent, bg="white")
    self.setupGUI()

  # sets up the GUI
  def setupGUI(self):
    # organize the GUI
    self.display = Label(self, text="", anchor=E,\
                         bg="white", height=2, font=("", 50))
    self.display.grid(row=0, column=0, columnspan=4, sticky=E+W+N+S)

    for row in range(1):
      Grid.rowconfigure(self, row, weight=1)
    for col in range(3):
      Grid.columnconfigure(self, col, weight=1)

    # calibrate
    button = Button(self, bg="white", \
                    borderwidth=0, highlightthickness=0,\
                    activebackground="white", text="Calibrate")
    button.grid(row=0, column=0, sticky=N+S+E+W)

    # start
    button = Button(self, bg="white", \
                    borderwidth=0, highlightthickness=0,\
                    activebackground="white", text="Start")
    button.grid(row=0, column=1, sticky=N+S+E+W)

    # stop
    button = Button(self, bg="white", \
                    borderwidth=0, highlightthickness=0,\
                    activebackground="white", text="Stop")
    button.grid(row=0, column=2, sticky=N+S+E+W)

    self.pack(fill=BOTH, expand=1)

    #sonar = CoordinateSystem(window)
    
    
    '''
    # setup input on the right side of the screen
    Sensor.player_input = Entry(self, bg="white")
    Sensor.player_input.bind("<Return>", self.process)
    Sensor.player_input.pack(side=RIGHT, expand=True, fill=BOTH)
    Sensor.player_input.focus()

    # setup the display on the left of the GUI
    sonar = CoordinateSystem(window)
    Sensor.sonar = Label(self, width=WIDTH / 2)
    Sensor.sonar.sonar = sonar
    Sensor.sonar.pack(side=LEFT, fill=Y)
    Sensor.sonar.pack_propagate(False)

    # setup buttons on the right side
    '''
    
  # process the input
  def process(self, event):
    pass

####################################
# setup GUI
####################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Sonar Sonic Sensor")

# creat the GUI as a Tkinter canvas inside the window
s = Sensor(window)
c = CoordinateSystem(window)

####################################
# rotate the sonar sensor and take distance measurements
####################################
#spin()
distances = [ 5, 6, 7, 8, 9, 10, 11, 12 ]

####################################
# calculate 2D points with distances
####################################

points = [Point(1,5), Point(5,5), Point(55, 55), Point(25, 75)] # example list

####################################
# plot 2D points to GUI
####################################
  # pass in a list of points

# wait for the window to close
window.mainloop()


# NOTES
# We should just worry about text in the GUI for now
# We can add buttons to start and stop later
