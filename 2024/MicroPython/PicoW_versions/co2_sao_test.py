# Simple CO2 Air Quality "Stoplight"
# MicroPython Version
#
# Author: David Bryant (david@disquiry.com)
# Date: October 12, 2024
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
# This version is developed for MicroPython, as used on Raspberry Pi devices
# and comparable ones based on the RP2040 MCU family
#
# A MicroPython port of Adafruit's SCD40 Circuit Python library is used for sensor
# communications and needs to be loaded onto the target device for
# the application to function.  That library allows setting the operating
# altitude, which should be defined properly here.  It also supports a temperature
# offset value, which is 2.0 degrees C by default but might need to be different
# depending on deployment environment.

import machine
from machine import Pin
import time
import scd4x
from measure import Measure

# Map LED control values (GPIO1 & GPIO2) to LED colors. Must agree with wiring
# on Stoplight controller board.  We're using a Grey code scheme for green ->
# yellow -> red as it seems likely green <-> yellow and yellow <-> red are the
# most likely transitions and so ideally should just be one bit different.
OFF = 0       # GPIO1 and GPIO2 both off
GREEN = 1     # GPIO1 on and GPIO2 off
YELLOW = 3    # GPIO1 and GPIO2 both on
RED = 2       # GPIO1 off and GPIO2 on

# Set sensor sample delay, in seconds.  Also used to determine whether SCD40
# can be used in low-power periodic mode or not (see SCD40 datasheet)
SAMPLE_DELAY = 40

# Specify altitude of measurement location, in meters
ALTITUDE = 400

# Define CO2 values (ppm) that constitute Red (Alarm) & Yellow (Warning) values
# US NIOSH (1987) recommendations:
# 250-350 ppm - normal outdoor ambient concentrations
# 600 ppm - minimal air quality complaints
# 600-1,000 ppm - less clearly interpreted
# 1,000 ppm - indicates inadequate ventilation; complaints such as headaches, fatigue, and eye and throat irritation will be more widespread; 1,000 ppm should be used as an upper limit for indoor levels

CO2_WARNING = 800
CO2_ALARM = 1000

# Get readings from the SCD40, which can report CO2, temperature & relative humidity
# Note that this blocks until the sensor reports it has data ready
def readscd4x():
    global scd4x
    
    while True:
        if scd4x.data_ready:
            tempF = (scd4x.temperature * 1.8) + 32.0
            # print("CO2: %d ppm" % scd4x.CO2)
            # print("Temperature: %0.1f *C" % scd4x.temperature)
            # print("Humidity: %0.1f %%" % scd4x.relative_humidity)
            # print()
            return scd4x.CO2, tempF, scd4x.relative_humidity
        else:
            time.sleep(1);
    
# Determine air quality corresponding to CO2 reading, with thresholds
# to establish green, yellow, and red status in overall PPM.  Note that
# these thresholds are somewhat arbitrary and not based on firm guidance.
def co2status(co2value):
    # AQ status is green if CO2 < WARNING level
    if co2value < CO2_WARNING:
        return GREEN
    # AQ status is yellow if WARNING <= CO2 < ALARM levels
    if co2value < CO2_ALARM:
        return YELLOW
    # AQ status is red if CO2 >= ALARM level
    return RED

# Set the stoplight LEDs based on CO2 status.  Attempts to minimize value
# flickering by (a) not changing outputs if the value hasn't changed and
# (b) using a gray code approach as described above
def setLED(newstatus):
    global _co2_status
    if newstatus == _co2_status:
        return
        
    if newstatus & 1:
        _led_bit0.value(1)
    else:
        _led_bit0.value(0)
    if newstatus & 2:
        _led_bit1.value(1)
    else:
        _led_bit1.value(0)
    _co2_status = newstatus
    return

def init():
    global scd4x,_led_bit0, _led_bit1, _co2_status
    
    # On-board LED, which isn't used normally but might be useful for debugging
    # led = Pin("LED", Pin.OUT)

    # The two GPIO lines for the SAO interface drive our Green/Yellow/Red LEDs.
    # status0 reflects  the low-order bit (GPIO1) and status1 is the high-order bit
    # (GPIO2) in our overall 2-bit encoding scheme.
    # 
    # Take care in mapping pin numbers silkscreened on the board to actual GPIO pin
    # IDs.  It's best to refer to the pinout for the MCU in use.  For example,
    # pins identified as "5" (D5) and "6" (D6) on the Adafruit Feather RP2040
    # itself are actually GPIO7 and GPIO8 (so must be identified as "7" and "8" \
    # respectively in calls to the MicroPython Pin() class.
    _led_bit0 = Pin(14, Pin.OUT)
    _led_bit1 = Pin(15, Pin.OUT)

    # Initialize LEDs to all off, overall CO2 status is off
    _led_bit0.value(0)
    _led_bit1.value(0)
    _co2_status = OFF

    # Connect to SCD40 and initialize
    # i2c = machine.I2C(1)  # For using the Feather RP2040 built-in STEMMA QT connector
    # Raspberry Pi Pico W use the below
    sdaPIN=machine.Pin(0)
    sclPIN=machine.Pin(1)
    i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
    scd4x = scd4x.SCD4X(i2c)


    # Make sure measurement is stopped so we can properly configure
    # the SCD40 and control which measurement mode to use
    scd4x.stop_periodic_measurement()
    print("Serial number:", [hex(i) for i in scd4x.serial_number])

    # Configure SDCD40 for local use. Must do before starting measurement
    scd4x.temperature_offset = 0.0
    scd4x.altitude = ALTITUDE

    # Can use low-power measurement mode for sampling longer than 30 seconds
    if SAMPLE_DELAY > 30:
        scd4x.start_low_periodic_measurement()
    else:
        scd4x.start_periodic_measurement()
        
    print("Waiting for first measurement....")

def main():
    init()
    counter = 0
    co2data = Measure()
    while True:
        # Read data from the SCD40, blocking until it has data
        co2value,tempF, relative_humidity = readscd4x()
        counter = counter + 1
        
        # Accumulate lastest data
        co2data.include(co2value)
        
        print("#%d: %d CO2 ppm, %0.1f *F, %0.1f %%RH  (CO2: %d->%d->%d)" % 
                (counter,co2value, tempF, relative_humidity,
                 co2data.getMinimum(),co2data.getAverage(), co2data.getMaximum()))
        
        # Calculate green/yellow/red CO2 air quality status from CO2 value
        newstatus = co2status(co2value)
        
        # Set status, which may result in updating stoplight LEDs
        setLED(newstatus)

        # Sleep for a chunk of the sample delay period (though the SCD40 runs on its own
        # sampling clock
        time.sleep(SAMPLE_DELAY/4)
        
if __name__=="__main__":
    main()
