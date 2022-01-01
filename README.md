# Netatmo-Python-Waveshare-Display
Crap of code to display all informations from the Netatmo API on a Waveshare e-Ink display.


Use the Netatmo API to display the current weather data from your Netatmo weather station on an e-Ink display.
These scripts make it possible to generate the current values on a Waveshare 7.5 inch display.
This allows you to build a very economical display for the current data.
(Low power consumption - No burn in of the display possible)


# But before you start, here are some important infos!
- This is currently code junk. It may work, but it doesn't have to.
- I have 0.0% Python skills. If you want to make it easier, faster and nicer, feel free to improve it!
- It was developed for the following display: epd7in5b V3
- Netatmo API → Python is required (https://github.com/philippelt/netatmo-api-python).
- The latest drivers for the Waveshare display are needed (https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python)
- A setup with a Raspberry Pi and the appropriate adapter for the display is needed
- I am german, so there are some german comments in the code. Maybe it helps you, or not

# What do you have to do?
1. install your hardware and Python3
2. create an API account at Netatmo
3. install the Netatmo API → Python tools from Philipp and store your access data
4. put the file "execute-code-json.py" in the folder of Netatmo-API-Python
5. in the folder "examples" of waveshare put the file "display.py"
6. put the file arrow.bmp in the folder "pics"
7. put the file "update-display.sh" somewhere and adjust the paths
8. run update-display.sh
9. hope that everything works ...


Helpful links:
- https://github.com/philippelt/netatmo-api-python/blob/master/usage.md
- https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)
- https://dev.netatmo.com/
