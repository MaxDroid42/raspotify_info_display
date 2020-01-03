# Info-Display for Raspotify

It will be frustrating to follow this guide. Sorry!<br>
*Note: it is using the HDMI-output of the Pi*<br>
**Also note: it is rather slow (tested on RPi Model B 1st gen. which is overclocked to 900 Mhz and has 128 MB of vram) and insecure!**

## Installation
* Install pip3 ```sudo apt install python3-pip```
* Put the script metadata_by_track_id.py (https://github.com/MaxDroid42/spotify_metadata) in the same directory as track_info.py<br>

*I put everything in the folder /home/pi/metadata for which this script is already configured!*

* Install fbi using ```sudo apt install fbi```

* Install dependencies for metadata_by_track_id.py:
  * lxml ```sudo apt install python3-lxml```
  * re ```sudo pip3 install re```

* Install dependencies for track_info.py:
  * Install dependencies for Pillow (PIL) ```sudo apt install libwebpmux3 liblcms2-2 libzstd1 libwebp6 libwebpdemux2 libtiff5 libopenjp2-7 libjbig0``` (see https://www.piwheels.org/project/Pillow/)
    * Install pillow itself ```sudo pip3 install Pillow```
    
## Setup
1. Change the OPTIONS-line using ```sudo nano /etc/default/raspotify``` to:<br>
```OPTIONS="--onevent 'python3 /home/pi/metadata/track_info.py'"```

2. Give the user "raspotify" the privilege to run killall and fbi:
<br>2.1. Run ```sudo visudo``` (maybe make a backup of that file befor) and add the following lines:<br>
```Cmnd_Alias FBI_CMD = /usr/bin/fbi --noverbose -T 1 -d /dev/fb0 /home/pi/metadata/cache/current_info.png```
*This is the alias for the fbi-command raspotify will be able to run.*<br>
```Cmnd_Alias KILL_CMD = /usr/bin/killall -9 fbi```<br>
*This is to kill the fbi-process because otherwise you would have multiple fbi-process overlaping each other.*
<br>2.2. Add this to the file:<br>
```raspotify ALL=(ALL) NOPASSWD: FBI_CMD, KILL_CMD```

3. Create the file-structer
<br>3.1. Create a metadata-folder which contains both scripts and a folder called "cache", which stores the album-cover and the final info-screen.
<br>3.2. Give the metadata folder the permission 755 usinf ```sudo chmod -R 755 metadata```
<br>3.3. Give the cache folder the permission 777 using ```sudo chmod 777 cache```<br>
*Those permissions should not be needed to be that high, but i experienced errors using lower permissions.*<br>
*THOSE PERMISSIONS ARE THE REASON WHY THIS SCRIPT IS SO INSECURE! (...and because of the extra privileges you give to raspotify)*
