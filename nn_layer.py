import numpy as np


class Layer:
    def __init__(self,n_inputs,n_neurons):
        self.weights = np.random.randn(n_inputs,n_neurons)
        self.biases = np.zeros(n_neurons)

    def forward(self, inputs):
        self.output = relu(np.dot(inputs,self.weights)+self.biases)
        return self.output


def relu(x):
    return np.maximum(0, x)