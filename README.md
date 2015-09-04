# Using Kivy with the official Raspberry Pi Touch Screen

The guide below and example code will get you started setting up the Raspberry Pi touch screen and getting Kivy working with it. [Kivy](http://kivy.org/) is an "open source Python library for rapid development of applications
that make use of innovative user interfaces, such as multi-touch apps." This guide assumes you're using a fresh install of Raspbian (2015-05-05 release), an Internet connection, and have the screen connected and working. It also assumes that you're already familiar with Raspberry Pi to get yourself to the command line, which you can do locally or via SSH. The command line is where you'll start.

1. Update your software. This is required with the 2015-05-05 Raspbian image in order to get touch working. This step will take a few minutes:

        pi@raspberrypi ~ $ sudo apt-get update && sudo apt-get -y upgrade

2. Reboot:

        pi@raspberrypi ~ $ sudo reboot

3. Back on the command line, check that touch input works by trying it in X11:

        pi@raspberrypi ~ $ startx

4. If touch works, exit out of X11 and go back to the command line.
5. The next few steps will install Kivy. These instructions are based on the [Kivy User’s Guide](http://kivy.org/docs/installation/installation-rpi.html). Firstly, open the APT sources list:

        pi@raspberrypi ~ $ sudo nano /etc/apt/sources.list

6. At the end of file, add the APT sources for Gstreamer:

        deb http://vontaene.de/raspbian-updates/ . main

7. Type `Control+X` to exit nano. Then press `Y` and `Enter` to save the file. You'll be back on the command line.

8. Download and add the GPG key for the Gstreamer sources (If you get an error, `gpg: keyserver receive failed: bad URI`, just try to run the command again. You should see `gpg: imported: 1`):

        pi@raspberrypi ~ $ gpg --recv-keys 0C667A3E
        pi@raspberrypi ~ $ gpg -a --export 0C667A3E | sudo apt-key add -

9. Install the dependencies:

        pi@raspberrypi ~ $ sudo apt-get update
        pi@raspberrypi ~ $ sudo apt-get -y install pkg-config libgl1-mesa-dev libgles2-mesa-dev \
        python-pygame python-setuptools libgstreamer1.0-dev git-core \
        gstreamer1.0-plugins-{bad,base,good,ugly} \
        gstreamer1.0-{omx,alsa} python-dev

10. Install pip from source (not sure if/why it must be from source and not via apt). You can ignore any messages about `InsecurePlatformWarning`:

        pi@raspberrypi ~ $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
        pi@raspberrypi ~ $ sudo python get-pip.py

11. Install [Cython](http://cython.org/), [Pygments](http://pygments.org/), and [docutils](https://pypi.python.org/pypi/docutils). The Pygments and docutils packages are not actually required for Kivy, but the example code we'll execute uses them. This step will take a few minutes:

        pi@raspberrypi ~ $ sudo pip install cython pygments docutils

12. Download Kivy and install it globally (this step will take quite a few minutes):

        pi@raspberrypi ~ $ git clone https://github.com/kivy/kivy
        pi@raspberrypi ~ $ cd kivy
        pi@raspberrypi ~/kivy $ python setup.py build
        pi@raspberrypi ~/kivy $ sudo python setup.py install

13. To enable touch, you'll need to make a modification to the Kivy configuration file:

        pi@raspberrypi ~/kivy $ nano ~/.kivy/config.ini

14. Go into the `[input]` section, remove the lines that are in there and put in:

        %(name)s = probesysfs,provider=mtdev

15. Reboot again.

16. Launch the multi touch pictures demo. Tap, drag, pinch, and rotate should all work like a dream:

        pi@raspberrypi ~ $ python ~/kivy/examples/demo/pictures/main.py

17. Type `Control+C` to exit the pictures demo.

18. Launch the UI showcase. This shows you all the different UI elements that Kivy makes available to you:

        pi@raspberrypi ~ $ python ~/kivy/examples/demo/showcase/main.py

19. If you'd like, explore the other examples in `~/kivy/examples/`.

20. To try Kivy and GPIO together, download this repo to your Raspberry Pi if you haven't already:

        pi@raspberrypi ~ $ git clone https://github.com/mrichardson23/rpi-kivy-screen.git

21. The example uses BCM GPIO pins 17 as a piezo buzzer, 27 as an LED, and 22 as a button (pulled HIGH, so connect one leg of the button to 22 and the other to ground.)

22. First try to run the example as root (root access is required for the GPIO library):

        pi@raspberrypi ~ $ cd rpi-kivy-screen/
        pi@raspberrypi ~/rpi-kivy-screen $ sudo python main.py 

22. As you'll see, touch doesn't work! To fix this, you need to make the same change to `config.ini` we made before, but to the root account's config file. Exit (`Control+C`) and copy over your home directory's Kivy configuration file to overwrite the root account's: 

        pi@raspberrypi ~/rpi-kivy-screen $ sudo cp ~/.kivy/config.ini /root/.kivy/config.ini

23. Run the example again and you'll be able to control the LED and buzzer. You'll also be able to see the state of the physical button!

        pi@raspberrypi ~/rpi-kivy-screen $ sudo python main.py 