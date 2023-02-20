import math

class pixel:
    index:int = 0
    x:float = 0.0 # horizontal location, in any unit
    y:float = 0.0 # vertical location, in any unit

    # private variables (that are calculated after loading into a set)
    __heading__:float = None

    def __init__(self, index:int, x:float, y:float) -> None:
        self.index = index
        self.x = x
        self.y = y

class space:

    def __init__(self, pixels:list[pixel], center_point:tuple[float, float] = None) -> None:

        # create the list of pixels variable
        self.__pixels__:list[pixel] = None

        # create the min and max's variables
        self.__max_x__:float = None
        self.__max_y__:float = None
        self.__min_x__:float = None
        self.__min_y__:float = None

        # set the pixels
        self.__pixels__ = pixels

        # calculate the mins and maxes
        for pix in pixels:

            # max x?
            if self.__max_x__ == None or pix.x > self.__max_x__:
                self.__max_x__ = pix.x
            
            # max y?
            if self.__max_y__ == None or pix.y > self.__max_y__:
                self.__max_y__ = pix.y

            # min x?
            if self.__min_x__ == None or pix.x < self.__min_x__:
                self.__min_x__ = pix.x
            
            # min y?
            if self.__min_y__ == None or pix.y < self.__min_y__:
                self.__min_y__ = pix.y

        # set the headings
        if center_point != None:
            for pix in self.__pixels__:
                pix.__heading__ = measure_heading(center_point, (pix.x, pix.y))


    # provide PERCENTAGES as each of the variables. Returns a list of int (indexes)
    def select_box(self, left:float, right:float, bottom:float, top:float) -> list[pixel]:

        # get ranges
        range_x = self.__max_x__ - self.__min_x__
        range_y = self.__max_y__ - self.__min_y__

        # mins and maxs of our selection
        min_x:float = left * range_x
        max_x:float = right * range_x
        min_y:float = bottom * range_y
        max_y:float = top * range_y

        # select
        ToReturn:list[pixel] = []
        for pix in self.__pixels__:
            if pix.x >= min_x and pix.x <= max_x and pix.y >= min_y and pix.y <= max_y:
                ToReturn.append(pix)

        return ToReturn

    # x and y are meant to be a PERCENT (between 0.0 and 1.0)
    def select_nearest(self, point:tuple[float, float]) -> pixel:

        # convert the inputs (percents) to an actual
        ax:float = point[0] * (self.__max_x__ - self.__min_x__)
        ay:float = point[1] * (self.__max_y__ - self.__min_y__)
        
        
        # find nearest
        NEAREST:pixel = None
        NEAREST_DISTANCE:float = float("inf")
        for pix in self.__pixels__:
            d:float = measure_distance((pix.x, pix.y), (ax, ay))
            if d < NEAREST_DISTANCE:
                NEAREST_DISTANCE = d
                NEAREST = pix

        return NEAREST

    # inputs are percentages
    # tolerance is how far (as a percentage) any particualr pixel can be "out of the line" (outside of DIRECTLY in between) and still be considered to be part of the line. Will need a higher tolerance when fewer pixels are present since those will be more "blocky" lines.
    def select_line(self, p1:tuple[float, float], p2:tuple[float, float], tolerance:float) -> list[pixel]:

        # get the pixels for each
        pix1:pixel = self.select_nearest(p1)
        pix2:pixel = self.select_nearest(p2)

        # measure the distance between these two
        line_length:float = measure_distance((pix1.x, pix1.y), (pix2.x, pix2.y))
        
        # loop through each one and see if it falls within this line
        ToReturn:list[pixel] = []
        ToReturn.append(pix1)
        ToReturn.append(pix2)
        for pix in self.__pixels__:
            if pix != pix1 and pix != pix2:
                dp1:float = measure_distance((pix.x, pix.y), (pix1.x, pix1.y))
                dp2:float = measure_distance((pix.x, pix.y), (pix2.x, pix2.y))
                if abs((dp1 + dp2) - line_length) < (line_length * tolerance): # 5% tolerance of differences
                    ToReturn.append(pix)

        return ToReturn

    def select_heading(self, heading_start:float, heading_stop:float) -> list[pixel]:
        ToReturn:list[pixel] = []

        for pix in self.__pixels__:
            if heading_stop > heading_start: # normal
                if pix.__heading__ >= heading_start and pix.__heading__ <= heading_stop:
                    ToReturn.append(pix)
            else: #this crosses over the 360/0 degree middle point
                if pix.__heading__ >= heading_start or pix.__heading__ <= heading_stop:
                    ToReturn.append(pix)

        return ToReturn

            
            
    
######### toolkit below ########


def measure_distance(p1:tuple[float, float], p2:tuple[float, float]) -> float:
    distance:float = math.sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))
    return distance
            
def measure_heading(center:tuple[float, float], subject:tuple[float, float]) -> float:

    # deal with fringe scenarios - scenarios where the subject is directly on one of the axes
    if center == subject:
        return 0
    if subject[0] == center[0]:
        if subject[1] > center[1]:
            return 0
        elif subject[1] < center[1]:
            return 180
    elif subject[1] == center[1]:
        if subject[0] > center[0]:
            return 90
        elif subject[0] < center[0]:
            return 270

    c:float = measure_distance(center, subject) #distance (hypotenuse)

    # handle by quadrant
    radians:float = None
    degrees_to_add:float = 0
    if subject[0] > center[0] and subject[1] > center[1]:
        radians = math.asin((subject[0] - center[0]) / c)
    elif subject[0] > center[0] and subject[1] < center[1]:
        radians = math.asin((center[1] - subject[1]) / c)  
        degrees_to_add = 90 
    elif subject[0] < center[0] and subject[1] < center[1]:
        radians = math.asin((center[0] - subject[0]) / c)
        degrees_to_add = 180
    elif subject[0] < center[0] and subject[1] >= center[1]:
        radians = math.asin((subject[1] - center[0]) / c)
        degrees_to_add = 270
        
    # convert radians to degrees
    degrees:float = radians * 57.2958
    degrees = degrees + degrees_to_add
    return degrees



    

        

