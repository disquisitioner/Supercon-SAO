# Printed Circuit Board Designs

Part of the fun and challenge of building a Supercon badge add-on is designing a printed circuit board (PCB) to use in assembling the add-on.  I've only ever designed and built one  PCB and that was a decade ago as part of taking a class on PCB design.

Happily tools for PCB design have gotten better and freely available as open source.  Among the SAO add-on community there was lots of love for [KiCad](https://www.kicad.org/), so I gave it a try.  The getitng started documentation is very helpful, taking you through the process of designing a schematic for the PCB, laying out the board itself, using tools to check the designs, and previewing everything before submitting it for manufacture. 

Even so, PCB design is a iterative process with lots of learn by doing, which means sending designs out for fabrication and discovering what you didn't quite get right when the boards come back.  Happily getting boards produced is quick and not particularly expensive!

The KiCad files are available here. 

## Schematic
![Add-on schematic](/2024/assets/CO2-SAO-schematic.png)
Using the two GPIO digital lines in the SAO add-on interface to control the three LEDs in the "stoplight" requires some simple digital logic to translate the four possible values of those two lines taken together (00, 01, 10, and 11) into separate single lines that drive the LEDs. That's easily done through a combination of Boolean "and" and "not" gates, but for a variety of reasons it's more commonly the case that "nand" gates (for "not-and") are used.  It would take three "and" and three "not" gates (inverters) to do the logic translation, but if done with "nand" gates you need eight overall.  Happily the 7400 digital logic IC incorporates four nand gates into a single 14-pin package, so two of those ICs get the job done.

If you're not familar with digital logic see if you can determine from the schematic how the "nand" gates make it work.


## PCB Layout
![Add-on PCB layout](/2024/assets/CO2-SAO-PCB.png)
