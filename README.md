# raspberry_ADS-B

With a fresh install of Noobs (after Wifi setup, updates, etc.), plug in a ADS-B USB receiver, open up a terminal...

```
cd ~
sudo apt-get update && apt-get upgrade
sudo apt-get install git
git clone https://github.com/sunsetmountain/raspberry_ADS-B
cd raspberry_ADS-B
chmod +x initialsoftware.sh
./initialsoftware.sh
```

Update the JSON keyfile name in batchGCS.py

Test dump1090

/home/pi/dump1090/dump1090 --net --interactive
