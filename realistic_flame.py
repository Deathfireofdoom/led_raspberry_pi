import random
import numpy as np







class Flame(object):
    def __init__(self, size=60, cooling=10):
        self.cooling = cooling
        self.cells = np.zeros(size)
        print(self.cells)

    def burn(self, spark_cells=[0, 1, 2], threshold=0.5, explosion_heat=[200, 300]):
        while True:
            if random.random() < threshold:
                self.cells[random.sample(spark_cells, 1)] = random.randint(*explosion_heat)
            self.calculate_temperature()

    def calculate_temperature(self, span=2):
        for i in range(len(self.cells)):
            self.cells[i] = np.average(self.cells[max(0, i-span):span]) - self.cooling




if __name__ == '__main__':
    flame = Flame()
    flame.burn()
