# Supercon 2024 Badge Add-On Project

My 2024 Supercon badge add-on is a real-time CO2 monitor with simple "stoplight" display of overall air quality using red, yellow, and green LEDs.  CO2 as a component of overall air quality isn't much talked about and health-specific requirements seem more advisory than proscriptive, but there's movement to do more in both monitoring and reducing CO2 especially in indoor settings.

This is my first Supercon and my first attempt at crafting a Supercon badge add-on, but it builds on [considerable work](https://github.com/ericklein/rco2) I've been doing with [@ericklein](https://github.com/ericklein/) exploring ways to easily measure and report [air quality](https://github.com/ericklein/air_quality) based on a wide variety of sensor inputs.

The CO2 monitor add-on we've built is based on:
* The Sensirion SCD40 true CO2 sensor, in particular the [Adafruit packaged version](https://www.adafruit.com/product/5187), which is small, accurate, supports I2C via either Qwiic connectors or dedicated wiring, provides additional on-board components for ease of use, and has mounting holes that allow it to be piggy-backed on a larger overall board or enclosure.
* Red, yellow and green rectangular LEDs with a thin outer case and diffuser, allowing them to be grouped into a single status bar, specifically [these](https://www.lumex.com/led-thru-hole-rect-1.html).
* Simple digital logic that translates the SAO connector's two GPIO digital inputs into control for the three LEDs. For me this is a delightful throwback to my college Electrical Engineering days almost exactly fifty years ago.  I know I could do this in other ways, e.g. with a smart RGB LED, but wanted to re-experience low-level digital design.
* Programming in Python with a a guess that we'd have an RP2040 main processor on the badge itself. Design and development of the add-on started in late September, about a month before Supercon but more significantly several weeks before we had any idea what the conference badge would be like or be extensible through add-ons.

I used [KiCad](https://kicad.org) to design a printed circuit board (PCB) that could  directly mount the LEDs, digital logic circuit, and SAO badge connector and also support the SCD40 breakout board both via mounting holes and connection points for the I2C interface. I knew I'd need to build and test the add-on without actually having the badge in hand. That led to the design of a simple SAO breakout board PCB that could handle either a female SAO connector (to simulate the badge itself) or a male SAO connector (to simulate being an add-on).  KiCad projects for both are here as well.

I used one of my on-hand Adafruit Feather RP2040 boards as a stand-in for the badge. That made it possible to breadboard the CO2 add-on's LED logic and connect the SCD40 via Qwiic cables, increasing my confidence in attempting a PCB design.  Development of software for that prototype was begun in CircuitPython, which Adafruit supports for both the SCD40 and Feather RP2040, knowing I should be able to migrate to MicroPython if that's indeed what would be announced for the badge (as turned out to be the case).

## The CO2 Add-On (SAO)
Here's the fully-assembled CO2 SAO as we wore it during Supercon, showing both the "stoplight" red/yellow/green LEDs on the board underneath and the Adafruit SCD40x breakout board mounted atop.
![CO2 SAO Prototype](/2024/assets/CO2_SAO_v1.png)

## Working Prototype
This is the first working instance of the CO2 SAO printed circuit board, in this case just with the circuitry to drive the "stoplight" of red, yellow and green LEDs.  You can see the SCD40 CO2 sensor on its separate brekaout board, connected to the Pico W via a Qwiic connector.
![CO2 SAO Prototype](/2024/assets/co2sao.jpg)