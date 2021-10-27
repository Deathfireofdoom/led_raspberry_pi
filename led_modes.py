import time
from rpi_ws281x import Color, PixelStrip, ws

from COLORS import *


# LED strip configuration:
LED_COUNT = 150         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_RGBW


class Pixel(object):
    def __init__(self, color, pixel_id, strip):
        self.strip = strip
        self.color_raw = color
        self.color = Color(*color)
        self.pixel_id = pixel_id

    def light(self):
        self.strip.setPixelColor(self.pixel_id, self.color)


class LedStrip(object):
    """Class to control a SK6812 strip"""
    def __init__(self): # TODO add parameters input if needed.
        print('LedStrip Init.')

        self.led_count = LED_COUNT
        self.led_pin = LED_PIN
        self.led_freq_hz = LED_FREQ_HZ
        self.led_dma = LED_DMA
        self.led_brightness = LED_BRIGHTNESS
        self.led_invert = LED_INVERT
        self.led_channel = LED_CHANNEL
        self.led_strip = LED_STRIP
        self.strip = PixelStrip(self.led_count, self.led_pin, self.led_freq_hz,
                                self.led_dma, self.led_invert, self.led_brightness,
                                self.led_channel, self.led_strip)
        self.strip.begin()

        self.pixels = []
        for pixel_id in range(self.led_count):
            self.pixels.append(Pixel(color=DEFAULT_COLOR, pixel_id=pixel_id, strip=self.strip))

        self.update_strip()

    def update_pixel(self, color_code, pixel_id, brightness=None):
        self.pixels[pixel_id].color_raw = color_code
        self.pixels[pixel_id].color = Color(*color_code)
        self.update_strip()

    def update_strip(self):
        for pixel in self.pixels:
            pixel.light()
        self.strip.show()

    def light(self,  color_code, brightness=None):
        color = Color(*color_code)
        brightness = (brightness if brightness else self.led_brightness) # Todo make this work
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def warm_white(self, brightness=None):
        self.light(WARM_WHITE)

    def turn_off(self):
        self.light((0, 0, 0, 0))

    def thunder(self):
        self.light((255, 0, 0, 0))

    def gradient(self, color_code1, color_code2):
        color = color_code1
        color_distance = list(map(lambda c1, c2: c1 - c2, color_code1, color_code2))
        color_step = list(map(lambda c: c/self.strip.numPixels(), color_distance))
        print(color[0] + color_step[0])
        print(color)
        print(color_step)

        for i in range(self.strip.numPixels()):
            color_pixel = Color(int(color[0] - color_step[0] * i),
                          int(color[1] - color_step[1] * i),
                          int(color[2] - color_step[2] * i),
                          int(color[3] - color_step[3] * i))
            self.strip.setPixelColor(i, color_pixel)

        self.strip.show()


    def siren(self, speed=50):
        color = (0, 0, 0, 0)
        while True:
            for i in range(speed):
                color = (color[0], int(color[1] + i * 255/speed), color[2], color[3])
                self.light(color)
                time.sleep(0.5)
            for i in range(speed):
                color = (color[0], int(color[1] - i * 255/speed), color[2], color[3])
                self.light(color)
                time.sleep(0.5)

    def pulse(self, color_code1, color_code2, speed=10, times=10):
        color = color_code1
        color_distance = list(map(lambda c1, c2: c1 - c2, color_code1, color_code2))
        color_step = list(map(lambda c: c / self.strip.numPixels(), color_distance))

        print(color_distance)
        print(color_step)
        x = 0
        while x < times:
            print(x)
            for i in range(speed):
                color = (max(int(color[0] - i * color_step[0] / speed), 0), max(int(color[1] - i * color_step[1] / speed), 0),
                         max(int(color[2] - i * color_step[2] / speed), 0), max(int(color[3] - i * color_step[3] / speed), 0))

                print(color[3] - i * color_step[3] / speed)
                print(color)

                self.light(color)
                time.sleep(0.01)

                #print(i)
                #print(color_step)
                #print(int(color[1] + i * color_step[1] / speed))
                #print(color)


            for i in range(speed):
                color = (max(int(color[0] + i * color_step[0] / speed), 0), max(int(color[1] + i * color_step[1] / speed), 0),
                         max(int(color[2] + i * color_step[2] / speed), 0), max(int(color[3] + i * color_step[3] / speed), 0))

                print(color[3] - i * color_step[3] / speed)
                print(color)

                self.light(color)
                time.sleep(0.01)

            x += 1
        print(color_distance)
        print(color_step)


    def christmas_light(self):
        x = 0
        color1 = Color(255, 0, 0, 0)
        color2 = Color(0, 255, 0, 0)
        color = color1
        while x < 10:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
                if i % 2:
                    if color == color1:
                        color = color2
                    else:
                        color = color1
            time.sleep(1)
            self.strip.show()
            x += 1

    def wake_up_light(self):
        start_pixels = [0, len(self.strip.numPixels()) - 1]

        for i in range(10):
            for k in range(self.strip.numPixels()):
                self.strip.setPixelColor(k, Color(0, 0, 0, i*25))
            self.strip.show()
            time.sleep(1)

if __name__ == '__main__':
    led = LedStrip()
    led.wake_up_light()
