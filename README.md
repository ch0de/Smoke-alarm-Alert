Supplies

smoke alarm with signal wire. https://a.co/d/gAJd2rS
Smoke Alarm relay https://a.co/d/bbx4Oty
smoke alarm protection cage to prevent tampering/theft https://a.co/d/9cLkJJt
Raspberry pi pico w https://a.co/d/bfYASqF
Wire connecters (i use wago) https://a.co/d/csqiEOY

Install 

Find a good spot where power is accessible. (you may need an electrician to install power box if your not comfortable.)
Hard wire the smoke alarm and the relay to 120v.
connect the relay interconnect (red) to the smoke alarm interconnect.
Connect the relay orange (NO , normally open) to pin 4 on the Pi Pico w
connect the relay Blue (Common) to any Ground pin on the Pi Pico W
Provide power to the Pico
Place alarm wire guard and secure.

Program the Pico W

First update the firmware of the Pi Pico w https://a.co/d/6snHIRc
Download and install Thonny https://thonny.org/
using thonny Upload umail.py to the Pico https://github.com/shawwwn/uMail/blob/master/umail.py
open main.py make changes and upload to Pico
Lines 17 to 18 change your SSID, and Wifi password. make sure to keep it between the ` `
lines 20 to 24 enter your smtp server username password
line 24 you can enter as many email addresses as you like, Separated by a comma ,
if you want it to text your phone also you will have to find your Cell phone carriers email to text address. Example .For at&t it is phonenumber@txt.att.net
