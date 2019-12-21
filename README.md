# Raspberry Pi Zero Controlled DJI Tello Drone

I recently bought DJI Tello and was amazed on how much you can learn and do with this little drone since it offers the ability to program. To start my learning, I decided to take inspiration from one of my pet projects on [controlling a RaspberryPi rover with Xbox One S Bluetooth Controller](https://github.com/erviveksoni/xbox-raspberrypi-rover).
I took the same code base and extended it to control the Tello using a easy to use and well documented python library [TelloPy](https://github.com/hanyazou/TelloPy).

While working on this application, I thought it would be a really cool idea to mount the Raspberry Pi Zero on top of the Tello itself rather then using the zero as a base station and keeping it on the ground. 
<br/>
<img src="/images/drone_front.jpeg" alt="Tello with Raspberry Pi Zero" width="600" height="274" border="0" />
<br/>
Offcourse this adds additional weight to the drone (and reduce flying time) but for the application I am looking it was OK! Also, this gives me freedom of not carrying my laptop whenever I want to fly it using Xbox One S controller. Additionally this lays foundation for a few project ideas I have.

To make this project you will need both hardware and software skills some of which I also learned during the process but that's the point... you gotta start somewhere!

## Prerequisites
- Raspberry Pi Zero W
- [Xbox One controller](https://www.microsoft.com/en-us/p/xbox-wireless-controller/8t2d538wc7mn?cid=msft_web_collection&activetab=pivot%3aoverviewtab) Generation 2 or later which has bluetooth support
<br/><img src="images/controller.png" width="371" height="262"/>
- [DJI Tello](https://store.dji.com/product/tello)
- [WiFi Dongle](https://www.raspberrypi.org/products/raspberry-pi-usb-wifi-dongle/)
- Micro USB to USB Type A female adapter [something like this](https://www.amazon.com/CableCreation-Adapter-Compatible-Samsung-Function/dp/B01LXBS8EJ/)
- 5V Step-Up Power Module Lithium Battery Charging Protection Board
 <br/>![5V Step-Up Power Module Lithium Battery Charging Protection Board](/images/powerbankmodule.jpeg)
- 3.7V 1200mah LiPo battery (Try getting the size: 30mm x 63mm x 4.75mm so it fits nicely over the drone)
- 3D printed [Raspberry Pi Zero Tello mount](https://www.thingiverse.com/thing:4022999) and screws
  <br/>The file RPi_zero_mount.scad zero_mount on the link above does not have a provision to hold Raspberry Pi camera. I extended this design and added a [bracket to hold camera](/files/RPi_zero_mount_with_camera.scad).
- Male micro usb cable head. You can use any old micro usb cable and cut micro usb head along with a small length of wire.
<br/>![shell](/images/microusbshell.jpeg)
- Wires
- Solderign gun
- Optional for this project: Raspberry Pi Camera V2

## Hardware
#### Creating the LiPo Battery Module
We wont be using the USB output from the Tello to power our Raspberry Pi Zero for obvious reason :-). Lets create our own power source to power the Raspberry Pi Zero as well as a permanent setup to charge it.
 - Remove the USB Type A shell from the module carefully (You may need to use a plair). Ensure the +ve and -ve output points are visible on the chip.
 - Solder the micro usb wires -> black to the -ve and red to +ve output points.
 - Follow this [youtube link](https://www.youtube.com/watch?v=KB8S83aY35w) to solder the LiPo connector to the charging module. 
 - Check whether the inout and output are working from the above setup.
### Mounting Raspberry Pi Zero on Tello Mount
 - Assemble the 3D printed Raspberry Pi Zero Tello mount.
 - Optional: Connect the Raspberry Pi Zero Camera module to Raspberry Pi Zero
 - Mount the Raspberry Pi Zero on the 3D printed assembled mount. You can a combination of screw which fits into the mount and rubber bands (check the images).
 - Also connect the LiPo batter module and the Micro USB to USB Type A female adapter + Wifi dongle to the Raspberry Pi Zero.
<table height="200px">
<tr>
<td><img src="images/assembled_zero_mount.jpeg" width="300" height="137"/><td/>
<td><img src="images/assembled_zero_mount_2.jpeg" width="300" height="137"/><td/>
<tr/></table>

## Mounting the 3D Mount on Tello
 - Detach the canopy from Tello
 - Snap the 3D Printed case on top of the Tello 

