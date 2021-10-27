from led_modes import LedStrip


LED_STRIP = LedStrip()

COLOR1 = (0, 255, 0, 0)
COLOR2 = (0, 0, 255, 0)
COLOR3 = (255, 0, 0, 0)
COLOR4 = (0, 200, 0, 0)



if __name__ == '__main__':
    LED_STRIP.pulse(COLOR1, COLOR4)