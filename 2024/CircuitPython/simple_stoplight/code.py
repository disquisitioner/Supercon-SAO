# Simple Air Quality "Stoplight"
#
# Author: David Bryant (david@disquiry.com)
# Date: September 29, 2024
#
# This Python program reads current CO2 values from an SCD40 air quality sensor
# and translates the reading into a simple Red/Yellow/Green indication that
# can be used to drive three LEDs.
#
# It is designed to be compatible with the "SAO" connector interface built into
# Superconference badges to enable user-developed add ons.  That interface
# provides VCC, GND, I2C data (SCL & SDA) and two GPIO pins.  I2C is used to
# communicate with the SCD40 and the two GPIO pins allow four different values
# (00, 01, 10, and 11) to be processed by digital logic gates to drive the 
# red, yellow and green LEDs independently.
#
# Adjustable thresholds allow easy adjustment to the CO2 levels (in ppm) that
# define good (Green), warning (Yellow), and alert (Red).
#
# Adafruit's SCD40 Circuit Python library is used for sensor communications,
# and needs to be loaded onto the target Circuit Python-compatible MCU for
# the application to function.  That library allows setting the operating
# altitude, which should be defined properly here.  It also supports a temperature
# offset value, which is 2.0 degrees C by default but might need to be different
# depending on deployment environment.


import board
import digitalio
import time
import adafruit_scd4x

# Note that this blocks until the sensor reports it has data ready
def readco2():
    global scd4x
    
    while True:
        if scd4x.data_ready:
            tempF = (scd4x.temperature * 1.8) + 32.0
            print("%d CO2 ppm, %0.1f *F, %0.1f %%RH" % 
                (scd4x.CO2, tempF, scd4x.relative_humidity))
            # print("CO2: %d ppm" % scd4x.CO2)
            # print("Temperature: %0.1f *C" % scd4x.temperature)
            # print("Humidity: %0.1f %%" % scd4x.relative_humidity)
            # print()
            return scd4x.CO2
        else:
            time.sleep(1);
    
# Determine air quality corresponding to CO2 reading, with thresholds
# to establish green, yellow, and red status in overall PPM.  Note that
# these thresholds are arbitrary and not based on hard science.
def co2status(co2value):
    # AQ status is green if CO2 < WARNING level
    if co2value < CO2_WARNING:
        return GREEN
    # AQ status is yellow if WARNING < CO2 < ALARM levels
    if co2value < CO2_ALARM:
        return YELLOW
    # AQ status is red if CO2 >= ALARM level
    return RED
    
def setLED(newstatus):
    global status
    if newstatus == status:
        return
        
    if newstatus & 1:
        status0.value = True
    else:
        status0.value = False
    if newstatus & 2:
        status1.value = True
    else:
        status1.value = False
    status = newstatus
    return

# Map LED control values (GPIO1 & GPIO2) to LED colors.
# Must agree with wiring on Stoplight controller board.
OFF = 0
GREEN = 1
YELLOW = 3
RED = 2

# Set sensor sample delay, in seconds
SAMPLE_DELAY = 40

# Specify altitude of measurement location, in meters
ALTITUDE = 400

# Define CO2 values that constitute Red (Alarm) & Yellow (Warning) values
# US NIOSH (1987) recommendations:
# 250-350 ppm - normal outdoor ambient concentrations
# 600 ppm - minimal air quality complaints
# 600-1,000 ppm - less clearly interpreted
# 1,000 ppm - indicates inadequate ventilation; complaints such as headaches, fatigue, and eye and throat irritation will be more widespread; 1,000 ppm should be used as an upper limit for indoor levels

CO2_WARNING = 800
CO2_ALARM = 1000

# On-board LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Two GPIO lines for the SAO interface, drives our Green/Yellow/Red LEDs.
# status0 is the low-order bit and status1 is the high-order bit in our
# overall 2-bit encoding scheme.
status0 = digitalio.DigitalInOut(board.D5)
status0.direction = digitalio.Direction.OUTPUT

status1 = digitalio.DigitalInOut(board.D6)
status1.direction = digitalio.Direction.OUTPUT

# Initialize LEDs to all off, overall CO2 status is off (LEDs are off)
status0.value = False
status1.value = False
status = OFF

# Connect to SCD40 and initialize
# i2c = board.I2C()  # uses board.SCL and board.SDA
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
# print("Serial number:", [hex(i) for i in scd4x.serial_number])

# Configure SDCD40 for local use. Must do before starting measurement
scd4x.temperature_offset = 0.0
scd4x.altitude = ALTITUDE

# Can use low-power measurement mode for sampling longer than 30 seconds
if SAMPLE_DELAY > 30:
    scd4x.start_low_periodic_measurement()
else:
    scd4x.start_periodic_measurement()
    
print("Waiting for first measurement....")
    
while True:
    # Read data from the SCD40, blocking until it has data
    co2value = readco2()
    
    # Calculate green/yellow/red CO2 air quality status from CO2 value
    newstatus = co2status(co2value)
    
    setLED(newstatus)

    time.sleep(SAMPLE_DELAY)