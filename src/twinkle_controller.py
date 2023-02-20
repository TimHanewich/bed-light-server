import neopixel
import twinkle
import settings
import color_toolkit
import time




# PLAY
STOP:bool = False
STOPPED:bool = True #default needs to be true
def play(pixels:neopixel.Neopixel, brightness_step:float = 0.01, frames_at_peak:int = 6, max_brightness:float = 0.25, max_twinkle_count:int = settings.led_count, twinkle_chance:float = 0.0001, sleep_between_frames:float = 0.05):

    # set up orchestrator
    ORCHESTRATOR:twinkle.orchestrator = twinkle.orchestrator(settings.led_count)
    ORCHESTRATOR.brightness_step = brightness_step
    ORCHESTRATOR.frames_at_peak = frames_at_peak
    ORCHESTRATOR.max_brightness = max_brightness
    ORCHESTRATOR.max_twinkle_count = max_twinkle_count
    ORCHESTRATOR.twinkle_chance = twinkle_chance

    # Sleep between frames, adjustable, in seconds
    SLEEP_BETWEEN_FRAMES:float = sleep_between_frames

    # reset
    pixels.fill((0, 0, 0))
    pixels.show()

    # reset status and GO!
    global STOP
    global STOPPED
    STOP = False
    STOPPED = False
    while STOP == False:
        twinkles:list[twinkle.led_twinkle] = ORCHESTRATOR.next_frame()
        for t in twinkles:
            color_to_set:tuple[int, int, int] = color_toolkit.adjust_brightness(t.color, (1 - t.percent) * -1)
            pixels.set_pixel(t.led, color_to_set)
        pixels.show()
        time.sleep(SLEEP_BETWEEN_FRAMES)

    # mark as stopped
    STOPPED = True

# here is a comment