# Write your code here :-)
# SPDX-FileCopyrightText: 2021 Smankusors for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VL53L0X distance sensor with continuous mode.
# Will print the sensed range/distance as fast as possible.
import time

import board
import busio

import adafruit_vl53l0x
import neopixel

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# You will see the benefit of continous mode if you set the measurement timing
# budget very high, while your program doing something else. When your program done
# with something else, and the sensor already calculated the distance, the result
# will return instantly, instead of waiting the sensor measuring first.
PIXEL_PIN = board.NEOPIXEL  # pin that the NeoPixel is connected to
ORDER = neopixel.RGB  # pixel color channel order
BAD = (0, 255, 0)  # color to blink
WARN = (255, 255, 0)  # clear (or second color)
GOOD = (255,0,0)
DELAY = 0.25  # blink rate in seconds

# Create the NeoPixel object
pixel = neopixel.NeoPixel(PIXEL_PIN, 1, pixel_order=ORDER)
#pixel[0] = COLOR
# Main loop will read the range and print it every second.
with vl53.continuous_mode():
    while True:
        # try to adjust the sleep time (simulating program doing something else)
        # and see how fast the sensor returns the range
        time.sleep(1)

        if vl53.range > 300:
            pixel[0] = GOOD
            print("GOOD")
        else:
            if vl53.range < 200:
                pixel[0] = BAD
                print("BAD")
            else:# vl53.range > 250 and vl53.range<150:
                pixel[0] = WARN
                print("WARN")


        curTime = time.time()
        print("Range: {0}mm ({1:.2f}ms)".format(vl53.range, time.time() - curTime))
