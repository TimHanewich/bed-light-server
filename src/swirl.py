import neopixel_spatial.spatial
import spatial_tools

# create the space
space:neopixel_spatial.spatial.space = neopixel_spatial.spatial.space(spatial_tools.bed_set(), (0, 0))

width:float = 10.0
increment:float = 2.0

# create the segments
print("Generating segments...")
segments:list[list[neopixel_spatial.spatial.pixel]] = []
heading_start:float = 0.0
distance_traveled:float = 0.0
while distance_traveled < 360.0:

    # select and add
    segment:list[neopixel_spatial.spatial.pixel] = space.select_heading(heading_start, heading_start + width)
    segments.append(segment)

    # increment
    heading_start = heading_start + increment
    distance_traveled = distance_traveled + increment



# create the pixels
import neopixel
import settings
pixels = neopixel.Neopixel(settings.led_count, 0, settings.led_pin, "GRB")
pixels.fill((0, 0, 0))
pixels.show()



# loop through each one to show
print("Infinite loop starting now... ")
import time
delay:float = 0.05 #delay time in between, in seconds
color = (0, 0, 255)
import neopixel_spatial.display
while True:
    for x in range(0, len(segments)):

        print("On cycle " + str(x) + "!")

        # current segment
        segment_current:list[neopixel_spatial.spatial.pixel] = segments[x]

        # last segment
        segment_last:list[neopixel_spatial.spatial.pixel] = None
        if x == 0:
            segment_last = segments[len(segments)- 1]
        else:
            segment_last = segments[x - 1]

        # turn the last one off
        print("Turning off segment... ")
        neopixel_spatial.display.display(pixels, segment_last, (0, 0, 0))

        # turn the current one on
        print("Turning on segment... ")
        neopixel_spatial.display.display(pixels, segment_current, color)

        # show
        pixels.show()

        # wait
        time.sleep(delay)

# comment