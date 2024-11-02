# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-wi-fi-micropython/

import machine
import network
from time import sleep
import scd4x

# Wi-Fi credentials
ssid = 'Supercon'
password = 'whatpassword'

# Init Wi-Fi Interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to your network
wlan.connect(ssid, password)

# Wait for Wi-Fi connection
connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    # raise RuntimeError('Failed to establish a network connection')
    print("Failed to establish a network connection")
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])
    

# sdaPIN=machine.Pin(0)
# sclPIN=machine.Pin(1)
# i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
i2c0 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
i2c1 = I2C(1, sda=Pin(26), scl=Pin(27), freq=400_000)

devices = i2c0.scan()
if len(devices) != 0:
    print('Number of I2C Bus 0 devices found=',len(devices))
    for device in devices:
        print("Device Hexadecimal Address= ",hex(device))
else:
    print("No device found")
    
devices = i2c1.scan()
if len(devices) != 0:
    print('Number of I2C Bus 1 devices found=',len(devices))
    for device in devices:
        print("Device Hexadecimal Address= ",hex(device))
else:
    print("No device found")


CO2SAO_ADDRESS     = 0x62
i2cbusses = which_bus_has_device_id(CO2SAO_ADDRESS)
if len(i2cbusses) >= 1:
    scd4x = scd4x.SCD4X(i2cbusses[0])

# Make sure measurement is stopped so we can properly configure
# the SCD40 and control which measurement mode to use
scd4x.stop_periodic_measurement()
print("Serial number:", [hex(i) for i in scd4x.serial_number])
scd4x.start_low_periodic_measurement()
print("Waiting for first measurement....")


# Blink Pico W onboard LED
led = machine.Pin("LED",machine.Pin.OUT)
while True:
    if scd4x.data_ready:
        tempF = (scd4x.temperature * 1.8) + 32.0
        print("%d CO2 ppm, %0.1f *F, %0.1f %%RH" %
             (scd4x.CO2, tempF, scd4x.relative_humidity))
    else:
        sleep(1);
    # led.on()
    # sleep(1)
    # led.off()
    # sleep(1)
    
