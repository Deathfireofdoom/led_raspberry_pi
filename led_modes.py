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
        self.color = color
        self.pixel_id = str(pixel_id)

    def light(self):
        self.strip.setPixelColor(self.pixel_id, self.color)


class LedStrip(object):
    """Class to control a SK6812 strip"""
    def __init__(self): # TODO add parameters input if needed.
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
