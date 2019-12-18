# Raspberry Pi Zero Controlled DJI Tello Drone

I recently bought DJI Tello and was amazed on how much you can learn and do with this little drone since it offers the ability to program. To start my learning, I decided to take inspiration from one of my pet projects on [controlling a RaspberryPi rover with Xbox One S Bluetooth Controller](https://github.com/erviveksoni/xbox-raspberrypi-rover).
I took the same code base and extended it to control the Tello using a easy to use and well documented python library [TelloPy](https://github.com/hanyazou/TelloPy).

While working on this application, I thought it would be a really cool idea to mount the Raspberry Pi Zero on top of the Tello itself rather then using the zero as a base station and keeping it on the ground. 
<br/>
<img src="/images/drone_front.jpeg" alt="Tello with Raspberry Pi Zero" width="400" height="182" border="0" />
<br/>
Offcourse this adds additional weight to the drone (and reduce flying time) but for the application I am looking it was OK! Also, this gives me freedom of not carrying my laptop whenever I want to fly it using Xbox One S controller. Additionally this lays foundation for a few project ideas I have.

To make this project you will need both hardware and software skills some of which I also learned during the process but that's the point... you gotta start somewhere!

## Prerequisites
- Raspberry Pi Zero W
- [Xbox One controller](https://www.microsoft.com/en-us/p/xbox-wireless-controller/8t2d538wc7mn?cid=msft_web_collection&activetab=pivot%3aoverviewtab) Generation 2 or later which has bluetooth support
<br/>![Controller](/images/controller.jpg)
- [DJI Tello](https://store.dji.com/product/tello)
- [WiFi Dongle](https://www.raspberrypi.org/products/raspberry-pi-usb-wifi-dongle/)
- Micro USB to USB Type A female adapter [something like this](https://www.amazon.com/CableCreation-Adapter-Compatible-Samsung-Function/dp/B01LXBS8EJ/)
- 5V Step-Up Power Module Lithium Battery Charging Protection Board
 <br/>![5V Step-Up Power Module Lithium Battery Charging Protection Board](/images/powerbankmodule.jpeg)
- 3.7V 1200mah LiPo battery (Try getting the size: 30mm x 63mm x 4.75mm so it fits nicely over the drone)
- 3D printed [Raspberry Pi Zero Tello mount](https://www.thingiverse.com/thing:4022999) and screws
  <br/>The file RPi_zero_mount.scad zero_mount on the link above does not have a provision to hold Raspberry Pi camera. I extended this design and added a [bracket to hold camera](/files/RPi_zero_mount_with_camera.scad).
- Male micro usb shell
<br/>![shell](/images/microusbshell.jpeg)
- Wires
- Solderign gun

