import adafruit_ssd1306
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import serial
import time
from xbee import XBee

# Create the I2C interface
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear the display
disp.fill(0)
disp.show()

# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing objrect to draw on image
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Define some constants to allow easy resizing of shapes
padding = -2
top = padding
bottom = height - padding
x = 0

# Load default font
font = ImageFont.load_default()

# Open Serial Port
port = serial.Serial('/dev/ttyUSB0', 9600)

# Create XBee
xbee = XBee(port)

while True:

    # Fetch data from XBee 1
    xbee.remote_at(
        frame_id='\x01',
        dest_addr_long='\x00\x00\x00\x00\x00\x00\x00\x00',
        dest_addr='\x00\x0A',
        options='\x02',
        command='IS')
    r1 = xbee.wait_read_frame()
    t1c = (((r1['parameter'][0]['adc-0']/1023) * 3300) - 500) / 10
    t1f = t1c * 1.8 + 32

    xbee.remote_at(
        frame_id='\x01',
        dest_addr_long='\x00\x00\x00\x00\x00\x00\x00\x00',
        dest_addr='\x00\x0C',
        options='\x02',
        command='IS')
    r2 = xbee.wait_read_frame()
    t2c = (((r2['parameter'][0]['adc-0']/1023) * 3300) - 500) / 10
    t2f = t2c * 1.8 + 32

    # Write output
    draw.text((x, top + 0), "XBee A: " + str(t1f), font=font, fill=255)
    draw.text((x, top + 8), "XBee C: " + str(t2f), font=font, fill=255)

    # Display image
    disp.image(image)
    disp.show()
    time.sleep(10)