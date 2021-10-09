import time
from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_COUNT = 150         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_RGBW



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

    def light(self,  color, brightness=None):
        brightness = (brightness if brightness else self.led_brightness) # Todo make this work
        for i in range(self.strip.numPixels()):
            print('hello')
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def warm_white(self, brightness=None):
        warm_white = Color(0, 0, 0, 255)
        self.light(warm_white)


if __name__ == '__main__':
    led = LedStrip()
    led.warm_white()
