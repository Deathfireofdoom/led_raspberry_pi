from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from led_modes import LedStrip

app = Flask(__name__)
api = Api(app)

LED_STRIP = LedStrip()

class LedCustomizer(Resource):
    def __init__(self):
        super().__init__()


    def get(self):
        pixel_id = int(request.args.get('pixelid'))
        print(pixel_id)
        b, r, g, w = LED_STRIP.pixels[pixel_id].color_raw
        color = {'b': b, 'r': r, 'g': g, 'w': w}
        return jsonify(color)



    def post(self):
        i = int(request.args.get('i'))
        i_plus = int(request.args.get('iplus'))
        i_minus = int(request.args.get('iminus'))

        r = int(request.args.get('r'))
        g = int(request.args.get('g'))
        b = int(request.args.get('b'))
        w = int(request.args.get('w'))

        color_code = (b, r, g, w)

        for pixel_id in range(i - i_minus, i + i_plus):
            LED_STRIP.update_pixel(color_code, pixel_id)
        print(color_code)

#    def post(self, i, i_plus, i_minus, r, g, b, w):
#        for pixel_id in range(i - i_minus, i + i_plus):
#            print(pixel_id)




api.add_resource(LedCustomizer, '/ledcustomizer')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

