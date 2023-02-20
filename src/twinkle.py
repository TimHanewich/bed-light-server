import color_toolkit
import random

class led_twinkle:
    led:int = 0
    color:tuple[int, int, int] # the PURE color (full bright)
    percent:float = 0.0
    direction = False #false = on way down, true = on way up
    frames_at_peak_remaining:int = 0 # the number of frames at it's peak brightness that this twinkle has left

class orchestrator:

    # public settings
    led_count:int = 0
    twinkle_chance = 0.02 # chance of a twinkle being created on any unused LED at any moment (any frame)
    max_brightness = 0.5 # percent of the "ceiling" each color will reach
    max_twinkle_count = 3 # the maximum number of lights that can be twinkling at once
    brightness_step = 0.01 # the amount each led will be incremented/decremented at each step (percent)
    frames_at_peak = 6 # the number of frames each twinkle will last at its peak brightness

    #private variables
    __current_twinkles__:list[led_twinkle] = []

    def __init__(self, led_count:int) -> None:
        self.led_count = led_count

    def next_frame(self) -> list[led_twinkle]:

        # go through each of the current twinkles and increment/decrement
        ToRemove = [] # twinkles to remove (finished)
        for twinkle in self.__current_twinkles__:

            #going up
            if twinkle.direction == True: 
                if round(twinkle.percent, 2) < self.max_brightness: # we are still on the way up!
                    twinkle.percent = twinkle.percent + self.brightness_step
                else: # we have reached the top, so turn around
                    if twinkle.frames_at_peak_remaining > 0:
                        twinkle.frames_at_peak_remaining = twinkle.frames_at_peak_remaining - 1 # basically, do nothing and decrement the # of frames remaining here at the peak
                    else: # the # of frames remaining is over, so start going on the way down
                        twinkle.direction = False
                        twinkle.percent = self.max_brightness - self.brightness_step
            else: #going down
                if round(twinkle.percent, 2) > 0.0:
                    twinkle.percent = twinkle.percent - self.brightness_step
                else: # we have reached the bottom
                    twinkle.percent = 0
                    ToRemove.append(twinkle)

        # remove all those that were just set to be removed
        for tr in ToRemove:
            self.__current_twinkles__.remove(tr)


        
        # go through each LED, see if we should make a new twinkle
        for x in range(0, self.led_count):

            # is this one part of an already existing twinkle (has a led_twinkle)?
            already_twinkling = False
            for twinkle in self.__current_twinkles__:
                if twinkle.led == x:
                    already_twinkling = True

            # if this LED is NOT already twinkling, should we make it tinkle?
            if len(self.__current_twinkles__) < self.max_twinkle_count: # only consider this if we have capacity to add
                if already_twinkling == False:
                    r:float = random.random()
                    if r <= self.twinkle_chance: # probability of a recreation at any moment
                        twinkle = led_twinkle()
                        twinkle.led = x
                        twinkle.color = color_toolkit.random_color()
                        twinkle.percent = 0.0
                        twinkle.direction = True
                        twinkle.frames_at_peak_remaining = self.frames_at_peak
                        self.__current_twinkles__.append(twinkle)
        
        # return the twinkles we have
        return self.__current_twinkles__

# e = orchestrator(10)
# while True:
#     twinkles = e.next_frame()
#     for twinkle in twinkles:
#         print(str(twinkle.led) + " - " + str(round(twinkle.percent, 2)))
#     input("Ready for next?")