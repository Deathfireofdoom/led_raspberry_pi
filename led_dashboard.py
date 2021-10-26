from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from led_modes import LedStrip


app = Flask(__name__)
api = Api(app)

LED_STRIP = LedStrip()


class LedDashboard(Resource):
    def __init__(self):
        super().__init__()
        self.current_mode = 'off'
        self.current_brightness = (LED_STRIP.led_brightness // 255) * 100

    def get(self):
        response = {
            'mode': self.current_mode,
            'brightness': self.current_brightness
        }
        return jsonify(response), 200

    def post(self):
        mode = request.args.get('mode')
        brightness = int(request.args.get('brightness'))
        print(mode)
        print(self.current_mode != mode)

        if self.current_mode != mode:
            if mode == 'ww':
                print('hello')
                LED_STRIP.warm_white()
                self.current_mode = mode

            if mode == 'th':
                LED_STRIP.thunder()
                self.current_mode = mode

            if mode == 'off':
                LED_STRIP.turn_off()
                self.current_mode = 'off'

        if brightness != self.current_brightness:
            LED_STRIP.led_brightness = 255 * (brightness // 100)
            self.current_brightness = brightness

        LED_STRIP.update_strip()

        return Response(status=201)


api.add_resource(LedDashboard, '/led-dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
