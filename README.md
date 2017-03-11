# wol-packet-replicator
A python script that replicates the listens for UDP wake on lan packets from outside the network

This is a easy way of using wake on lan from outside the network when your router does not support forwarding ports to the broadcast address
I use it in a Raspberry Pi without problems so far, and it works great.

## Usage
1. Clone this repository: `git clone https://github.com/jaime29010/wol-packet-replicator
2. Install requirements: `pip install pyyaml`
3. Run it: `python replicator.py`

You will also want to assign your Raspberry Pi (or other) device a static IP, this is how I did it in mine
![DHCP Reservation](http://image.prntscr.com/image/c416ef2d45c640f6ac6cbc762d630389.png)

And of course, you will want forward the port
![Port Forwarding](http://image.prntscr.com/image/4fca48f3c4c641af82a4f31c9c71167c.png)

It is also recommended to setup DDNS on your router so you can connect to it without worrying about the public IP changing

After you have done that, you can just send the WOL packet to the you choose (in my case 5009)
You can test it with [this tool](http://www.wakeonlan.me/index.php)
Check the output of the script or the `app.log` file to see if it is working or not
