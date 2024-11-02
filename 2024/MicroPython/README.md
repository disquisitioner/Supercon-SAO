# MicroPython Work

The Supercon 2024 badge is [built](https://hackaday.com/2024/10/22/the-2024-hackaday-supercon-sao-badge-reveal/) around the Raspberry Pi Pico W, which is great as that means there's both a familar platform underneath the badge and whatever specialized software the conference folks design for it and there's a generalized development platform we can use to design, build, and test badge add-ons even without having a badge.

That said, the badge environment does have some unique properties that mean software developed to run on a Pico W running the standard MicroPython environment won't necessarily run (or run properly) on the badge itself.  Having only just gotten my badge today at day 1 of Supercon 2024, I'm still figuring out what those differences are and how to manage code mindful of them.

In the meantime I've resorted to developing and managing two different versions of the code that runs our CO2 add-on -- one that runs in a vanila MicroPython environment on the Pico W and one that runs on the badge with its own pre-defined boot and main operating program (boot.py and main.py respectively).

The Pico W side of things is quite straightfowrard.  Create a main.py file and it'll get loaded when the device powers up.  Otherwise the Python interpreter loads and you can run commands over the console built in to Thonny as the Python REPL.   During development when I have lots of different Python programs I might be editing and running (e.g. to test out wifi connectivity or I2C operations) I give them all obvious names and run them from within Thonny.

On the 2024 Supercon badge there's already a boot.py program that loads when the device boots, and a main.py program that's intended to be the default badge main program.  Together they enable a couple of add-ons that came with the badge at the conference, but they also provide some utilities that reflect badge hardware.  In particular the 2024 badge was built around having and exploring multiple add-ons. Instead of prior year's single add-on port the 2024 badge offers six add-on connectors, three each on the two I2C busses provided by the Pico W.

This means your 2024 badge addons need to be aware of two I2C busses and be flexible about figuring out which GPIO pins are connected to any particular add-on.  A convenience function provided in the badge's pre-installed boot.py helps find the right I2C bus for any device address but you're on your own determining which GPIO pins are connected to any particuclar add-on.

In this repo I've setup separate subfolders for code that's intended to be used on a generic Pico W or on the Supercon badge. I often have both environments available during development (especially during Badge Hacking Day at Supercon itself) so not getting confused about which code runs where is important.

Generally speaking what's in each subfolder is the proper variant of the following: 
* `fauxbadge.py` - An attempt to simulate the badge software itself, which I'm guessing will handle boot-time initialization for the badge hardware and then transition to a simple main loop for ongoing operation across whichever add-ons are installed.  Both initialization and main loop will be extensible in some way to allow add-ons to be easiy added and arranged.  Until we know more I'm trying to keep this as simple as possible.
* `co2sao.py` - A minimalistic handler for the CO2 monitor add-on, providing an initializing routine as well an update function called from the badge main loop to retrieve air quality information from the add-on's sensor and update the on-board LED status bar accordingly.
* `measure.py` - A utility module that makes it easy to track a time series of sensor data and determine minimum and maximum observed values, average value, number of samples, etc.
* `co2_sao_test.py` - A stand-alone program to interface with my CO2 add-on hardware directly without any assumptions about how the badge will actually work.  This was my starting point for add-on development before knowing anything about this year's badge hardware, and is still useful for easy testing of the add-on.

A few things work in both environments:
* `scd4x.py` - A MicroPython port of the Adafruit SCD4x CircuitPython library, courtesy of @peter-l5 on [GitHub](https://github.com/peter-l5/MicroPython_SCD4X).

## The CO2 Supercon Add-On (SAO)
Here's the fully-assembled CO2 SAO, showing both the "stoplight" red/yellow/green LEDs on the board underneath and the Adafruit SCD40x breakout board mounted atop.
![CO2 SAO Prototype](/2024/assets/CO2_SAO_v1.png)

## Current Working Prototype
This is the first working instance of the CO2 SAO printed circuit board, in this case just with the circuitry to drive the "stoplight" of red, yellow and green LEDs.  You can see the SCD40 CO2 sensor on its separate brekaout board, connected to the Pico W via a Qwiic connector.
![CO2 SAO Prototype](/2024/assets/co2sao.jpg)