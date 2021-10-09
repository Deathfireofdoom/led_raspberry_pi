from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from led_modes import LedStrip

app = Flask(__name__)
api = Api(app)


class LedCustomizer(Resource):
    def __init__(self):
        super().__init__()
        self.led_strip = LedStrip()


    def post(self):
        i = request.args.get('i')
        i_plus = request.args.get('iplus')
        i_minus = request.args.get('iminus')

        r = int(request.args.get('r'))
        g = int(request.args.get('g'))
        b = int(request.args.get('b'))
        w = int(request.args.get('w'))

        color_code = (b, r, g, w)

        for pixel_id in range(i - i_minus, i + i_plus):
            self.led_strip.light_pixel(color_code, pixel_id)
        print(color_code)

#    def post(self, i, i_plus, i_minus, r, g, b, w):
#        for pixel_id in range(i - i_minus, i + i_plus):
#            print(pixel_id)




api.add_resource(LedCustomizer, '/ledcustomizer')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

