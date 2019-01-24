import progressbar
import numpy as np

class Model:

    def __init__(self, layers):
        """
            :param layers: an odd list alterning Element-Exchange-Element-Exchange-...-Element
        """

        self.layers = []

        for i in range(0, len(layers), 2):
            self.layers.append(layers[i])

        for i in range(1, len(layers), 2):
            exchange = layers[i]
            exchange.prev_bloc = layers[i-1]
            exchange.next_bloc = layers[i+1]

            layers[i-1].set_next_exchange(exchange)
            layers[i+1].set_prev_exchange(exchange)

    def run(self, timestep=1e-3, time=30):

        steps = int(time / timestep)

        for _ in progressbar.progressbar(range(steps)):
            for layer in self.layers:
                layer.calc_next_step(timestep)

            for layer in self.layers:
                layer.go_next_state()


        return np.linspace(0, time, steps)

    def summary(self):
        layer = self.layers[0]
        exchange = None

        while layer is not None or exchange is not None:
            if layer is not None:
                print(layer)
                exchange = layer.next_exchange
                layer = None

            elif exchange is not None:
                print(exchange)
                layer = exchange.next_bloc
                exchange = None
