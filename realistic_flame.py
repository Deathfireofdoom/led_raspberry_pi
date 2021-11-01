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

    def explosion(self, heat=1200, number_of_explosion=3):
        for i in range(number_of_explosion):
            self.cells[i] = heat
        print([color == (0, 0, 0, 0) for color in self.cells])
        while not all([color == (0, 0, 0, 0) for color in self.cells]):
            self.calculate_temperature()
            sleep(0.01)



    def burn(self, spark_cells=[0, 1, 2], threshold=0.1, explosion_heat=[1000, 1200]):
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        while True:
            if random.random() < threshold:
                self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
            self.calculate_temperature()
            sleep(0.01)

    def calculate_temperature(self, span=2):
        for i in range(len(self.cells)):
            new_temp = np.average(self.cells[max(0, i-span):i + span])
            self.strip.setPixelColor(i, self.gradient.get_color(new_temp))
            self.cells[i] = max(0, new_temp - self.cooling) if not np.isnan(new_temp) else 0.0
        self.strip.show()




if __name__ == '__main__':
    flame = Flame()
    sleep(2)
    flame.explosion()
    sleep(2)
    flame.burn()
