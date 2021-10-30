import numpy as np
import random
from led_modes import LedStrip
from rpi_ws281x import Color
import time

LED_STRIP = LedStrip()

class Fire(object):
    def __init__(self, color_code1=(0, 166, 25, 0), color_code2=(0, 240, 100, 0)):
        color_distance = np.subtract(color_code2, color_code1)
        self.strip = LED_STRIP.strip

        self.sparks = [Spark(np.array(color_code1), color_distance) for _ in range(self.strip.numPixels())]

    def burn(self):
        for i, spark in enumerate(self.sparks):
            print(Color(*spark.next_color()), i)
            #self.strip.setPixelColor(i, Color(*spark.next_color()))
            self.strip.setPixelColor(i, Color(0, 166, 0, 0))


class Spark(object):
    def __init__(self, base_color, color_distance, threshold=0.5, speed_threshold=[10, 20], intensity_threshold=[0.5, 0.8]):
        self.base_color = base_color
        self.color_distance = color_distance
        self.threshold = threshold
        self.intensity_threshold = intensity_threshold
        self.speed_threshold = speed_threshold
        self.reset()

        for attr in dir(self):
            print(attr)
            print("obj.%s = %r" % (attr, getattr(self, attr)))

        time.sleep(5)

    def reset(self):
        self.alive = False
        self.speed = None
        self.intensity = None


    def next_color(self):
        if not self.alive and  self.threshold < random.random():
            print('yesss')
            self.start()
        
        if not self.alive:
            print(*tuple(self.base_color))
            return tuple(self.base_color)
        
        else:
            self.time_alive += 1
            if self.time_alive < self.speed / 2:
                print(self.color_distance * self.time_alive / self.speed)

                print(np.add(self.base_color, self.color_distance * self.time_alive / self.speed).astype(int))
                return tuple(np.add(self.base_color, self.color_distance * self.time_alive / self.speed).astype(int))
            else:
                tmp_color = np.add(self.base_color, self.color_distance * (self.speed - self.time_alive) / self.speed)
                if self.time_alive > self.speed:
                    self.reset
                print(tuple(tmp_color.astype(int)))
                print('esss')
                return tuple(tmp_color.astype(int))
            
            
            

    def start(self):
        self.alive = True
        self.time_alive = 0
        self.speed = random.randint(self.speed_threshold[0], self.speed_threshold[1])
        self.intensity = random.uniform(self.intensity_threshold[0], self.intensity_threshold[1])


if __name__ == '__main__':
    fire = Fire()
    while True:
        fire.burn()