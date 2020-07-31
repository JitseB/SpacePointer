# Space Pointer
My first combined hardware-software project! This device points to any object in space, whether that be a planet, an asteroid or a satellite.
The device is built around an old Raspberry Pi model b rev 2. Using some 3d-printed parts, a servo (MG90S) and a stepper motor (NEMA17) it can point any position in space. A slip ring (KW-2380) makes sure the cables do not get tangled up.

*The code and 3d models for this project is not optimized and could use some minor tweaking.*

## Internet functionality
As the device is built around a raspberry pi, it is possible to create functionalities based around internet. For this project that means that the standard objects are updated when an ethernet cable is connected. When a crosslink cable is connected to the device (and a laptop), one can access the website of the device. On this website (see fig. 1), you can change several variables, most important of which is the ability to change the object to track. This differentiates the space pointer from any basic ISS pointer which I was originally planning on making.

### Website screenshot
Figure 1:

![Website](https://i.imgur.com/uR0SQuG.png)

## Object data format
The software is written in Python using a library called pyephem. This is quite an old library which acts as a wrapper for a legacy C library (libastro). (For a future project I'd rather use Skyfield as this is completely written in Python and uses numpy for its calculations). This gives some limitation to adding new objects to the list:
* You can use the **xephem format**. Example: [Comets data](https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt)
* You can use **two-line-element sets (TLEs)**. Example: [Satellite data](https://celestrak.com/NORAD/elements/stations.txt)

The TLEs are for earth orbiting objects, the db format of xephem can be for any celestial object.

The planets that are included in the space pointer software are provided by the pyephem library by default.

### Sites (from https://www.clearskyinstitute.com/xephem/help/xephem.html#Download)
*""Several particularly useful sites as of this build are already entered. The first three are from Dr. TS Kelso's Earth satellite lists at [celestrak.com](http://www.celestrak.com/). The other four are the Minor Planet Center's lists of hot comets and unusual asteroids specially formatted for [XEphem](http://cfa-www.harvard.edu/iau/Ephemerides/Soft03.html). Click Get beside the desired catalog to download the file to the Private directory and simultaneously load into XEphem memory.""*

## Setup
Setting up the device is very simple. Before powering the device, one has to point the arm to true north. This can be done with any basic GPS-compass. (The true north is calculated via the magnetic north plus/minus the magnetic deviation). Once this action is finished, connect the crosslink cable to your laptop/pc and the device can be powered using a micro-usb power supply! The device will make a few movements to make sure it can rotate, after which it will point to the tracking object.

Once the hardware is setup, the first time you open the website interface you'll be asked to input the time. Format: MM/DD/YYY HH:mm (sadly we have to use the illogical US format because of the linux disto). This will change the date of the device and make sure it's pointing in the right direction.

A picture of the device can be seen in figure 2.

### Hardware
Figure 2:

![Device](https://i.imgur.com/ucTYsWF.png)

### LED codes
The device has 3 LEDs. These encode the following messages:
* **Green LED**: The tracking object is overhead and can be seen.
* **Red LED**: The tracking object never comes above the horizon or the selected custom object data cannot be interpreted.
* **Yellow LED**: When connected to internet, this LED lights up when the standard objects are being updated and the LAN cable should not be disconnected.

## License
This project is licensed under the MIT license.
