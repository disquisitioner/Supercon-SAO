import machine
import network
from time import sleep
import scd4x
import basicdweet
import co2sao

# Wi-Fi credentials
ssid = 'Centaurus A'
password = 'P@ran0rm@l'

def badge_init():
    global wlan
    
    # Scan for attached I2C devices
    sdaPIN=machine.Pin(0)
    sclPIN=machine.Pin(1)
    i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
    devices = i2c.scan()
    if len(devices) != 0:
        print('Number of I2C devices found =',len(devices))
        for device in devices:
            print("    I2C Device at address = ",hex(device))
    else:
        print("No device found")
        
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
        raise RuntimeError('Failed to establish a network connection')
    else:
        network_info = wlan.ifconfig()
        print('WiFi connected, IP address:', network_info[0])

def init():
     # Initialize the badge itself
     badge_init()
     
     # Initialize all add-ons
     co2sao.init()
     
def main():
    # Initialize everything
    print("Badge initializing...")
    init()
    
    # Main loop
    print("Beginning main loop")
    while True:
        # Call update functions for all attached add-ons
        co2sao.update()
        sleep(10)
    
        
if __name__=="__main__":
    main()