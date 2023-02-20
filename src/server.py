import socket
import network
import time
import server_tools
import request_tools
import json
import settings
import neopixel
import machine
import twinkle_controller
import _thread
import neopixel_spatial
import neopixel_spatial.spatial
import neopixel_spatial.display
import spatial_tools

# first, blink the LED twice
# please note that this is the way to do it for the Raspberry Pi Pico W... providing 'LED' as  the pin number.
led = machine.Pin("LED", machine.Pin.OUT)
led.on()
time.sleep(0.5)
led.off()
time.sleep(0.5)
led.on()
time.sleep(0.5)
led.off()

# create the pixels
pixels = neopixel.Neopixel(settings.led_count, 0, settings.led_pin, "GRB")
pixels.fill((0, 0, 0))
pixels.show()


# create the spatial
spatial_set:list[neopixel_spatial.spatial.pixel] = spatial_tools.bed_set()
space:neopixel_spatial.spatial.space = neopixel_spatial.spatial.space(spatial_set, (0.0, 0.0))


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while wlan.isconnected() == False:

    # little blip of the LED light to indicate we are trying
    led.on()
    time.sleep(0.1)
    led.off()

    print("Connecting...")
    print("SSID: '" + settings.wlan_ssid + "'")
    print("Pass: '" + settings.wlan_password + "'")
    wlan.connect(settings.wlan_ssid, settings.wlan_password)
    time.sleep(3)

# connected!
led.on() # indicates we are connected!
print("Connected!")
my_ip:str = str(wlan.ifconfig()[0])
print("My IP Address: " + my_ip)

# create socket
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

# Listen
print("Now listening")
while True:
    cl, addr = s.accept()

    try:
        
        # Read
        request:bytearray = request_tools.read_all(cl, 100, 2.5)

        # parse
        req:request_tools.request = request_tools.request.parse(request.decode())
        print("Body length: " + str(len(req.body)))
        
        # handle it differently based upon what the requestor wants
        # a simple get request means they are trying to request the webpage. So show the webpage and that is it
        # a POST request means that they are trying to send a command (via JSON).
        if req.method.lower() == "get":
            # respond with the webpage
            cl.send("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + server_tools.get_html())
            cl.close()
        elif req.method.lower() == "post":

            # Stop twinkle if it is ongoing
            if twinkle_controller.STOPPED == False:
                twinkle_controller.STOP = True # tell it to stop
                while twinkle_controller.STOPPED == False:
                    time.sleep(0.25) # wait until it is confirmed as stopped

            # parse the body
            command = json.loads(req.body)
            mode:str = command["mode"]

            if mode == "rgb":
                r:int = command["r"]
                g:int = command["g"]
                b:int = command["b"]

                # if a heading is specified in the JSON object, read it
                h0:float = None
                h1:float = None
                if "h0" in command and "h1" in command:
                    h0 = command["h0"] # heading start
                    h1 = command["h1"] # heading stop

                # if a specific heading range was specified, respect it and do that range only
                if h0 != None and h1 != None:
                    heading_range:list[neopixel_spatial.spatial.pixel] = space.select_heading(h0, h1) # select range
                    neopixel_spatial.display.display(pixels, heading_range, (r, g, b)) # fill
                else: # a heading range was not specific, so fill all of them
                    pixels.fill((r, g, b)) # fill all of them

                # Show!
                pixels.show()
                
            elif mode == "twinkle":

                brightness_step:float = command["brightness_step"]
                frames_at_peak:int = command["frames_at_peak"]
                max_brightness:float = command["max_brightness"]
                max_twinkle_count:int = command["max_twinkle_count"]
                twinkle_chance:float = command["twinkle_chance"]
                sleep_between_frames:float = command["sleep_between_frames"]

                _thread.start_new_thread(twinkle_controller.play, (pixels, brightness_step, frames_at_peak, max_brightness, max_twinkle_count, twinkle_chance, sleep_between_frames))

            # respond with OK
            cl.send("HTTP/1.0 200 OK\r\n\r\n")
            cl.close()
    
    except Exception as e:

        print("Critical failure! Msg: " + str(e))

        # respond with OK
        cl.send("HTTP/1.0 500 INTERNAL SERVER ERROR\r\n\r\n")
        cl.close()

    


    
    
    