from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from led_modes import LedStrip
from realistic_flame import Flame
from fire import Fire

from threading import Thread

app = Flask(__name__)
api = Api(app)

LED_STRIP = LedStrip()


current_mode = 'off'
print('yeee')

current_brightness = (LED_STRIP.led_brightness // 255) * 100

class ColorPicker(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        pass #TODO Add function to send back color

    def post(self):
        r = int(request.args.get('r')) #Todo fix weird bug R switch place with G
        g = int(request.args.get('g'))
        b = int(request.args.get('b'))
        w = int(request.args.get('w'))
        print((g, r, b, w))
        LED_STRIP.light((g, r, b, w))

global
threads = []

class LedDashboard(Resource):
    def __init__(self):
        super().__init__()
        self.flame = Flame()
        self.fire = Fire()

    def get(self):
        global current_mode
        global current_brightness
        response = {
            'mode': current_mode,
            'brightness': current_brightness
        }
        return jsonify(response), 200

    def post(self):
        global current_mode
        global current_brightness

        mode = request.args.get('mode')
        brightness = int(request.args.get('brightness'))
        print(mode)
        print(current_mode != mode)

        if current_mode != mode:
            print('ess')
            print(self.threads)
            for thread in threads:
                print('eyesesa')
                thread.stop()

            if mode == 'ww':
                thread = Thread(target=self.fire.burn()).start()
                threads.append(thread)
                #LED_STRIP.warm_white()
                current_mode = mode

            if mode == 'th':
                thread = Thread(target=self.flame.burn()).start()
                threads.append(thread)
                #LED_STRIP.thunder()

                current_mode = mode

            if mode == 'off':
                LED_STRIP.turn_off()
                current_mode = 'off'

            if mode == 'xmas':
                LED_STRIP.christmas_light()

            if mode == 'gr':
                c1 = (150, 0, 0, 0)
                c2 = (0, 150, 0, 0)
                LED_STRIP.gradient(c1, c2)

            if mode == 'sy':
                LED_STRIP.siren()

        if brightness != current_brightness:
            LED_STRIP.led_brightness = 255 * (brightness // 100)
            current_brightness = brightness

        return Response(status=201)


api.add_resource(LedDashboard, '/led-dashboard')
api.add_resource(ColorPicker, '/color-picker')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
