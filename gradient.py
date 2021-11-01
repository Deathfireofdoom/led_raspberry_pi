from collections import namedtuple
from rpi_ws281x import Color

GradientColor = namedtuple('GradientColor', 'color location')


class Gradient(object):
    def __init__(self, colors, density=2000, span_length=100):
        self.density = density
        self.span_length = span_length
        self.colors = colors
        self._calculate_density_multiplier()
        self._calculate_gradient()

    def get_color(self, index):
        gradient_index = max(min(round(
            (index / self.span_length) * len(self.gradient)),
            len(self.gradient) - 1),
            0)
        return self.gradient[gradient_index]

    def _calculate_density_multiplier(self):
        span_top = self.colors[-1].location
        self.density_multiplier = int(self.density / span_top)

    def _calculate_gradient(self):
        self.gradient = []
        for i_span in range(len(self.colors) - 1):
            self.gradient += self._calculate_span(i_span)

    def _calculate_span(self, i_span):
        start_color = self.colors[i_span]
        end_color = self.colors[i_span + 1]
        steps = end_color.location * self.density_multiplier - start_color.location * self.density_multiplier
        color_distance = list(map(lambda c1, c2: c1 - c2, end_color.color, start_color.color))
        color_step = list(map(lambda c: c/steps, color_distance))

        span = []
        for i in range(steps):
            next_color = tuple((
                            start_color.color[0] + color_step[0] * i,
                            start_color.color[1] + color_step[1] * i,
                            start_color.color[2] + color_step[2] * i,
                            start_color.color[3] + color_step[3] * i))
            next_color = tuple(map(lambda c: int(min(max(0, c), 255)), next_color))
            span.append(Color(next_color[0], next_color[1], next_color[2], next_color[3]))
        return span


class FireGradient(Gradient):
    def __init__(self):
        self._fire_colors()
        super().__init__(colors=self.colors, span_length=1500, density=1500)

    def _fire_colors(self):
        self.colors = []
        self.colors.append(GradientColor(color=(0, 0, 0, 0), location=0))
        self.colors.append(GradientColor(color=(0, 0, 0, 0), location=300))
        self.colors.append(GradientColor(color=(0, 142, 0, 0), location=600))
        self.colors.append(GradientColor(color=(64, 254, 0, 0), location=800))
        self.colors.append(GradientColor(color=(164, 254, 0, 0), location=900))
        self.colors.append(GradientColor(color=(253, 255, 164, 0), location=1100))
        self.colors.append(GradientColor(color=(243, 229, 254, 0), location=1500))



if __name__ == '__main__':
    color1 = GradientColor(color=(0, 0, 0, 0), location=0)
    color1 = GradientColor(color=(0, 0, 0, 0), location=200)
    color2 = GradientColor(color=(0, 255, 0, 0), location=300)
    color3 = GradientColor(color=(0, 0, 255, 0), location=500)
    color4 = GradientColor(color=(0, 0, 0, 255), location=1300)
    colors = [color1, color2, color3, color4]

    gradient = Gradient(colors, span_length=1300)

    fg = FireGradient()

