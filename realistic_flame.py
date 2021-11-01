import random
import numpy as np
from time import sleep
from led_modes import LedStrip



from gradient import FireGradient






class Flame(object):
    def __init__(self, size=60, cooling=10):
        self.strip = LedStrip().strip
        self.cooling = cooling
        self.cells = np.zeros(size)
        self.gradient = FireGradient()


    def burn(self, spark_cells=[0, 1, 2], threshold=0.5, explosion_heat=[1500, 1600]):
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        while True:
            #if random.random() < threshold:
            #    self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
            self.calculate_temperature()

    def calculate_temperature(self, span=2):
        for i in range(len(self.cells)):
            new_temp = np.average(self.cells[max(0, i-span):i + span])
            self.strip.setPixelColor(i, self.gradient.get_color(new_temp))
            self.cells[i] = max(0, new_temp - self.cooling) if not np.isnan(new_temp) else 0.0





if __name__ == '__main__':
    flame = Flame()
    flame.burn()
