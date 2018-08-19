# Install all of the core software needed to make use of a SDR (software defined radio)

# Start at the beginning by going home.
cd ~

# Make sure everything is up-to-date and then install core packages
sudo apt-get update
sudo apt-get -y install git cmake python-pip python-dev build-essential libusb-1.0-0.dev
sudo pip install --upgrade pip pyasn1

# Git rtl-sdr
git clone https://git.osmocom.org/rtl-sdr
cd rtl-sdr

# cmake projects are compiled from source with a build directory you must create.
mkdir build && cd build

# Run cmake for the parent directory
# with the -DINSTALL_UDEV-RULES=ON argument, we don’t need to mess with any of the udev stuff because a /etc/udev/rules.d/rtl-sdr.rules file was already created.
cmake ../ -DINSTALL_UDEV_RULES=ON

# In typical UNIX fasion, we compile from source using ./install.sh && make && sudo make install
# but with cmake projects, subsititute that install.sh part with cmake
# So we need to do the other two parts.
make && sudo make install

# For good measure, let’s do an ldconfig
sudo ldconfig

# Create /etc/modprobe.d/blacklist-rtl.conf without opening a text editor!
sudo bash -c “echo ‘blacklist dvb_usb_rtl28xxu’ >/etc/modprobe.d/blacklist-rtl.conf”

# Install GPRX prebuilt for Raspberry Pi 3 (latest link is always at http://gqrx.dk/download/gqrx-sdr-for-the-raspberry-pi)
cd ~
curl -SL https://github.com/csete/gqrx/releases/download/v2.9/gqrx-2.9-linux-armv6.tar.xz | tar xJv

sudo apt-get -y install gnuradio libvolk1-bin libusb-1.0-0 gr-iqbal qt5-default libqt5svg5 libportaudio2

# You need to run volk_profile for the user that is going to use this program.
volk_profile

# Install dump1090 script
cd ~
git clone https://github.com/antirez/dump1090
cd dump1090
make

# Change back to original directory to finish off the install
cd ~
cd raspberry_ADS-B
sudo pip install -r requirements.txt

# Install Google Cloud packages
sudo pip install --upgrade google-cloud-storage
sudo pip install --upgrade oauth2client

# Create a data directory
cd ~
mkdir rawData

# Add startup commands to the end of .profile
echo "/home/pi/dump1090/dump1090 --net &" >> /home/pi/.profile
echo "python /home/pi/raspberry_ADS-B/1090Parser.py &" >> /home/pi/.profile
echo "python /home/pi/raspberry_ADS-B/batchGCS.py &" >> /home/pi/.profile
