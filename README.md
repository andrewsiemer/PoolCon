## PoolCon1
#### An affordable IoT pool controller for Embedded Systems Design graduate course.

### Objective
Allow a pool owner to monitor and control essential pool equipment with a low-cost and universal add-on.

### Technical Details
The controller is a combined Raspberry Pi and Arduino hybrid system. The Raspberry Pi hosts the web service and process tasks, while the Arduino does real-time sensor data and relay control.

### Results
The system can be controlled from a user's smartphone or desktop. The entire system costs less than 1/10th of a base brand name unit with similar functionality.

![OC-graphic](/static/graphic.jpeg)

### The PoolCon1 Team
* Andrew Siemer - Electrical/Software Engineer
* Jacob Button - Electrical/Software Engineer
* Kyla Tarpey - Electrical Engineer

---

## Detailed Design

The objective of this document is to demonstrate that the PoolCon1 Team designed and created a product that provides solutions to all the requirements and constraints set forth for the Pool Controller Project. This document will outline the design process taken by the team that led to the final design. It will take into account the requirements, the available materials, the selected materials, and the implementation of the chosen materials that created the team’s end product. The document can be viewed or downloaded from the link below.

### [View Detailed Design Document](https://docs.google.com/document/d/1jAVQZhhNynOp6t5FPtTxNcznvJQWsQ1ORJpYy8FkHpE)

---

## Installation

> ***Warning:*** This system interacts with house power (120VAC), which is extremely dangerous if the correct safety precautions are not taken. Before operating around outlets, open and exposed circuits, and modules of this system, make sure to check the connection of the power and verify it is off before you begin installation. 
The Sensor Module for this system will be operating in your pool, so when installing this module, be careful not to expose the non-waterproofed components to high volumes of water. This module runs on low voltage (3.3VDC), and does not pose a severe electrocution threat. While this module does not pose a severe electrocution threat, you should still operate safely around any electronic system that functions near or in water.
PoolCon1 does not take responsibility for any accidents that occur in the installation and maintenance of this pool control system. Follow all applicable state and national Electrical codes in the installation of this system.

### System Parts List
* Pool Controller Unit
  * Internal: Control Board, Pool Pump Relay, Pool Heater Relay, Water Valve Relay
  * External: Air Temperature Sensor, Pool Temperature Sensor, Water Level Sensor, PH Sensor, ORP Sensor
* Remote Unit
* Mobile Remote (optional - your smartphone or computer)

### 1) Pool Controller Unit
The Pool Controller Unit comes completely assembled with the latest version of our software installed. All you need to do is connect your existing pool equipment and add your network file to the microSD card and plug it in!

***Before starting please disconnect all power!***

#### Mount Pool Controller Unit
The Pool Controller Unit comes with the proper mounting hardware or the waterproof box. Mount the box with the wires coming out the bottom against a wall near the pool equipment. It is important that the hole that the wires are coming out of is facing down.
Connect to Pool Equipment
Now that the Pool Controller Unit is safely mounted to the wall, we can connect to the pool equipment. 

#### Pool Pump Relay
Locate the power wires of your Pool Pump. They should be Line, Neutral, & Ground. Now open the Pool Controller Unit and locate the terminal strip on the bottom wall. Screw the Pool Pump Ground wire to the terminal labeled (G). Next, screw the Pool Pump Neutral wire to the terminal labeled (N). Finally, screw the Pool Pump Line wire to the terminal labeled (1). Make sure all connections are secure before moving to the next step.

#### Pool Heater Relay
Locate the power wires of your Pool Heater. They should be Line, Neutral, & Ground. Screw the Pool Heater Ground wire to the terminal labeled (G). Next, screw the Pool Pump Heater wire to the terminal labeled (N). It is okay to put more than one (N) or (G) on the same terminal. Finally, screw the Pool Heater Line wire to the terminal labeled (2). Make sure all connections are secure before moving to the next step.

#### Water Valve Relay
Locate the power wires of your Water Valve. They should be Line, Neutral, & Ground. Screw the Water Valve Ground wire to the terminal labeled (G). Next, screw the Water Valve wire to the terminal labeled (N). It is okay to put more than one (N) or (G) on the same terminal. Finally, screw the Water Valve Line wire to the terminal labeled (3). Make sure all connections are secure before moving to the next step.

#### Water Temperature Sensor
The Water Temperature Sensor can easily be installed by inserting it into the nearest available pool water. Advanced install can insert it into a water pipe and seal the insertion hole.

#### Water Level Sensor
The Water Level Sensor can easily be installed by attaching it to the side wall of the pool. It should be mounted so that the mounting holes are just above the edge of the pool so that water would never be able to get above it.

#### PH Level Sensor
The PH Level Sensor can easily be installed by inserting it into the nearest available pool water. Advanced install can insert it into a water pipe and seal the insertion hole.

#### ORP Level Sensor
The ORP Level Sensor can easily be installed by inserting it into the nearest available pool water. Advanced install can insert it into a water pipe and seal the insertion hole.

#### Connect to your Network
Remove the microSD card from the control board inside the Pool Controller Unit. Plug the microSD card into your computer. Next open your favorite text editor and paste the following text.
```sh
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network ={
ssid="<Name of your wireless LAN>"
psk="<Password for your wireless LAN>"
} 
```

You will need to change three things: your country code, your wifi network ssid and the wifi network password (type NONE if you do not have a wifi password).

Once you have done the above steps, save the file as `wpa_supplicant.conf`. Then, locate the microSD card named `boot` and drag the file to the disk. Once this is done, you can safely remove the microSD card from your computer and put it back into the Pool Control Unit control board.

Now plug the Pool Control Unit into the wall outlet and you are good to go. Setup of the Pool Control Unit is now complete!

### 2) Remote Unit
The Remote Unit comes completely assembled with the latest version of our software installed. All you need to do is add your network file to the microSD card and plug it in!

***Before starting please disconnect all power!***

#### Connect to your Network
Remove the microSD card from the back side of the Remote Unit. Plug the microSD card into your computer. Next open your favorite text editor and paste the following text.
```sh
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network ={
ssid="<Name of your wireless LAN>"
psk="<Password for your wireless LAN>"
} 
```

You will need to change three things: your country code, your wifi network ssid and the wifi network password (type NONE if you do not have a wifi password).

Once you have done the above steps, save the file as `wpa_supplicant.conf`. Then, locate the microSD card named `boot` and drag the file to the disk. Once this is done, you can safely remove the microSD card from your computer and put it back into the back of the Remote Unit.

Now plug the Remote Unit into the wall outlet and you are good to go. Setup of the Remote Unit is now complete!

### 3) Mobile Remote
View the dashboard in your browser of any device on your local network by going to: 
```
http://poolcon1.local:8000
```

### Troubleshooting
We designed our system to be simple, affordable and extremely easy to use.

#### Internet Connection
To be certain that the devices are connected to the internet: Power them up, and wait to see if you can access the web service from your browser. 

View the dashboard in your browser of any device on your local network by going to: 
```
http://poolcon1.local:8000
```

If the web service does not show up after 2 minutes from the time it was plugged in, retry the Connect to your Network instructions.

### Conclusion
We designed this unit to be very easy to use and most installations are fairly simple. If you think something is not working as it should please reach out to us first!
