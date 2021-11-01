import random
import numpy as np
from time import sleep
from led_modes import LedStrip



from gradient import FireGradient






class Flame(object):
    def __init__(self, size=60, cooling=10):
        self.strip = LedStrip().light((0,0,0,0)).strip
        self.size = self.strip.numPixels()
        self.cooling = cooling
        self.cells = np.zeros(self.strip.numPixels())
        self.gradient = FireGradient()
        print(self.size)

    def explosion(self, heat=1700, number_of_explosion=10):
        for i in range(number_of_explosion):
            self.cells[i] = heat
        print([all(color == (0, 0, 0, 0)) for color in self.cells])
        while not all([all(color == (0, 0, 0, 0)) for color in self.cells]):
            self.calculate_temperature()
            sleep(0.005)


    def fire_place(self, height=10, threshold):
        pass


    def burn(self, spark_cells=range(20), threshold=1, explosion_heat=[900, 1000]):
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)

        while True:
            if random.random() < threshold:
                self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
            self.calculate_temperature()
            sleep(0.02)

    def calculate_temperature(self, span=2):
        for i in range(self.size//2):
            new_temp = np.average(self.cells[max(0, i-span):i + span])
            self.strip.setPixelColor(i, self.gradient.get_color(new_temp))
            self.cells[i] = max(0, new_temp - self.cooling) if not np.isnan(new_temp) else 0.0

            inverted_i = self.size - i - 1 - 17 #Since i did not set up my strip properly
            self.strip.setPixelColor(inverted_i, self.gradient.get_color(new_temp))
            self.cells[inverted_i] = max(0, new_temp - self.cooling) if not np.isnan(new_temp) else 0.0

        self.strip.show()




if __name__ == '__main__':
    flame = Flame()
    sleep(2)
    flame.explosion()
    sleep(2)
    flame.burn()
