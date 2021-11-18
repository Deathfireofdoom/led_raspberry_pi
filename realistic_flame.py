import random
import numpy as np
from time import sleep
from led_modes import LedStrip
import os
import glob


from gradient import FireGradient






class Flame(object):
    def __init__(self, size=60, cooling=5):
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


    def fire_place(self, height=10, threshold=0.2):
        pass

    def burn2(self, state_file_name='test', spark_cells=range(10), threshold=0.2, explosion_heat=[1000, 1200]):
        self.cooling = 10
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)

        while not os.path.isfile(state_file_name):
            if random.random() < threshold:
                self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
            self.calculate_temperature()
            sleep(0.001)
        return

    def burn(self, state_file_name, spark_cells=range(30), threshold=0.5, explosion_heat=[900, 1000]):
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
        self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)

        while os.path.isfile(state_file_name):
            if random.random() < threshold:
                self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
            self.calculate_temperature()
            sleep(0.02)
        return

    def calculate_temperature(self, span=2):
        for i in range(self.size//2):
            new_temp = np.average(self.cells[max(0, i-span):i + span])
            self.strip.setPixelColor(i, self.gradient.get_color(new_temp))
            self.cells[i] = max(0 if i > 30 else 600, new_temp - self.cooling) if not np.isnan(new_temp) else 0.0

            inverted_i = self.size - i - 1 - 17 #Since i did not set up my strip properly
            self.strip.setPixelColor(inverted_i, self.gradient.get_color(new_temp))
            self.cells[inverted_i] = max(0 if i > 30 else 600, new_temp - self.cooling) if not np.isnan(new_temp) else 0.0

        self.strip.show()

    def calculate_temperature2(self, span=2):
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
    #flame.explosion()
    flame.burn2()
