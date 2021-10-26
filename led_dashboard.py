from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from led_modes import LedStrip


app = Flask(__name__)
api = Api(app)

LED_STRIP = LedStrip()


current_mode = 'off'
print('yeee')

current_brightness = (LED_STRIP.led_brightness // 255) * 100

class LedDashboard(Resource):
    def __init__(self):
        super().__init__()

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
            if mode == 'ww':
                print('hello')
                LED_STRIP.warm_white()
                current_mode = mode

            if mode == 'th':
                LED_STRIP.thunder()
                current_mode = mode

            if mode == 'off':
                LED_STRIP.turn_off()
                current_mode = 'off'

        if brightness != current_brightness:
            LED_STRIP.led_brightness = 255 * (brightness // 100)
            current_brightness = brightness

        LED_STRIP.update_strip()

        return Response(status=201)


api.add_resource(LedDashboard, '/led-dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
