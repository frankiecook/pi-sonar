class Point(object):
    #constructor, defaults to 0,0 if not specified
    def __init__(self, xcoord = 0.0, ycoord = 0.0):
        self.xcoord = xcoord
        self.ycoord = ycoord
    
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
