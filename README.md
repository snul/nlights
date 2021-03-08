# nLights: Control your LED Strip with a Raspberry Pi and Apps for Android & iOS!

Just install this software on your Raspberry Pi, download the App from the AppStore/PlayStore and control your custom LED Lights!

Major features: 
- Control your custom LED Strip / Lights
- Free Apps for iOS and Android
- Support for RGB Led Strip
- Support for WS2812(B) / Neopixel 
- Webapplication coming soon!


## Apps

<a target="_blank" href="https://itunes.apple.com/us/app/nlights/id1406932079?l=de&ls=1&mt=8"><img alt="get it on google play" src="https://nlights.at/github/app-store-badge.png" width="200px"></a><br />
<a target="_blank" href="https://play.google.com/store/apps/details?id=net.snul.nlights"><img alt="get it on google play" src="https://nlights.at/github/google-play-badge.png" width="200px"></a>


## Installation

Install `git` and follow the instructions:
```console
sudo apt-get install git
or
sudo yum install git
```

### Setup and create a new user: 

```console
git clone https://github.com/snul/nlights.git
cd nlights
./setup.sh
```
### Start nLights in the background: 
```console
./start.sh
```

### Add to autostart: 
```console
sudo crontab -e
add: @reboot cd /path/to/nlights && ./start.sh
```

## Setup LED Strip with a Raspberry Pi

Thanks to David Ordnung for this tutorial in German & English:
[https://dordnung.de/raspberrypi-ledstrip/](https://dordnung.de/raspberrypi-ledstrip/)


### GPIO Mapping for Rasperry Pi Pins:
Should work with all Raspberry Pi Versions, Pins can be configured in the App. 
<img src="https://nlights.at/github/gpiomapping.png">


## Contact

If you have any issues, suggestions or whatever, please feel free to contact us: support@nlights.at

## Thanks for your support!
