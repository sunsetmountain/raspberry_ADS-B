# Install all of the core software needed to make use of a SDR (software defined radio)

# Start at the beginning by going home.
cd ~

# Make sure everything is up-to-date and then install core packages
sudo apt-get update
sudo apt-get -y install git cmake python-pip python-dev build-essential libusb-1.0-0.dev
sudo pip install --upgrade pip

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

# Plug in your SDR dongle and then reboot your raspberry pi
#sudo reboot
#rtl_test -t

# rtl_test may look like a failure, but what matters is it should find your device. If it does you should be all set.
# Download GQRX. There is a prebuilt binary for Raspberry Pi 3.
cd ~
curl -SL https://github.com/csete/gqrx/releases/download/v2.9/gqrx-2.9-linux-armv6.tar.xz | tar xJv

sudo apt-get -y install gnuradio libvolk1-bin libusb-1.0-0 gr-iqbal qt5-default libqt5svg5 libportaudio2

# You need to run volk_profile for the user that is going to use this program.
volk_profile
cd ~
cd raspberry_ADS-B
sudo pip install -r requirements.txt

# Install Google Cloud packages
sudo pip install --upgrade google-cloud-storage
sudo pip install --upgrade oauth2client
