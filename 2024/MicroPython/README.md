# MicroPython Work


After much anticipation and preparatory guesswork, the Supercon 2024 badge was finally officially [revealed](https://hackaday.com/2024/10/22/the-2024-hackaday-supercon-sao-badge-reveal/) on October 22, just ten days before the event.  Delightfully, this year's theme is all about making the most of the Supercon Add-on (SAO) expansion interface that has grown over the years to provide a flexible environrment for building new and novel devices that can operate onboard the event badge. Details on badge operation and programming are still not known, but the work is happening in an open [repository](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge) we can watch (and contribute to) over the days leading up to the conference.

Most of my speculation about the badge has proven true.  It'll be built around the Raspberry Pi Pico, specifically the Pico W which provides WiFi and Bluetooth support.  And it'll be programmed in MicroPython using the latest stable release.  What I didn't anticipate is that SAO programming is what the badge is all about.  The physical hardware is designed around a hexagonal shape that provides not just one add-on connection port as in past years -- but six!

As part of the SAO emphasis each badge will come with four add-ons, giving everyone a way to explore.  I'm still planning on builting something new that leverages real-time monitoring of air quality (especially CO2), and have enough information to get started on that while also anticipating critical details will become known between now and the first day of the conference (which is set aside as Badge Hacking Day).

I've acquired a couple of Raspberry Pi Pico W devices to use in gearing up.  A variety of aspects of that pre-conference preparation will accumulate here, so far including:

* `fauxbadge.py` - An attempt to simulate the badge software itself, which I'm guessing will handle boot-time initialization for the badge hardware and then transition to a simple main loop for ongoing operation across whichever add-ons are installed.  Both initialization and main loop will be extensible in some way to allow add-ons to be easiy added and arranged.  Until we know more I'm trying to keep this as simple as possible.
* `co2sao.py` - A minimalistic handler for the CO2 monitor add-on, providing an initializing routine as well an update function called from the badge main loop to retrieve air quality information from the add-on's sensor and update the on-board LED status bar accordingly.
* `scd4x.py` - A MicroPython port of the Adafruit SCD4x CircuitPython library, courtesy of @peter-l5 on [GitHub](https://github.com/peter-l5/MicroPython_SCD4X).
* `measure.py` - A utility module that makes it easy to track a time series of sensor data and determine minimum and maximum observed values, average value, number of samples, etc.
* `co2_sao_test.py` - A stand-alone program to interface with my CO2 add-on hardware directly without any assumptions about how the badge will actually work.  This was my starting point for add-on development before knowing anything about this year's badge hardware, and is still useful for easy testing of the add-on.

## Current Working Prototype
![CO2 SAO Prototype](/2024/assets/co2sao.jpg)