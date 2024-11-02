import machine
from machine import Pin
import time
import scd4x
import basicdweet

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

def init():
    global scd4x, _led_bit0, _led_bit1, _co2_status

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
    # print("Serial number:", [hex(i) for i in scd4x.serial_number])

    # Configure SDCD40 for local use. Must do before starting measurement
    scd4x.temperature_offset = 0.0
    scd4x.altitude = ALTITUDE

    # Can use low-power measurement mode for sampling longer than 30 seconds
    if SAMPLE_DELAY > 30:
        scd4x.start_low_periodic_measurement()
    else:
        scd4x.start_periodic_measurement()    

def update():
    global scd4x 
    if scd4x.data_ready:
            tempF = (scd4x.temperature * 1.8) + 32.0
            print("Hi: %d ppm CO2, %0.1f *F, %0.1f %%RH" % (scd4x.CO2,tempF,scd4x.relative_humidity))
            
            # Calculate green/yellow/red CO2 air quality status from CO2 value
            newstatus = co2status(scd4x.CO2)
            
            # Set status, which may result in updating stoplight LEDs
            setLED(newstatus)
            
            # Post latest readings via dweet.io (presuming we're connected to a network)
            postdweet(scd4x.CO2,tempF,scd4x.relative_humidity)
            
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

def postdweet(co2, tempF, rh):
    payload = {
        'co2': co2,
        'temperatureF' : tempF,
        'humidity' : rh
        }
    r = basicdweet.dweet_for('orangemoose-co2sao',payload)
    print(r)
