import numpy as np


class Neuron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)

    def start(self, inputs):
        return np.dot(self.weights, inputs)


class NeuralNetwork:
    def __init__(self):
        self.neurons = [Neuron(12), Neuron(12), Neuron(12), Neuron(12)]

    def calculate(self, inputs):
        return [
            self.neurons[0].start(inputs),
            self.neurons[1].start(inputs),
            self.neurons[2].start(inputs),
            self.neurons[3].start(inputs)
        ]
