"""
A module that consists of a neural network that can make predictions given inputs.

Author
----------
Adam Skudlarek

Classes
----------
NeuralNetwork:
    Makes predictions based off of input.

"""
import math
import numpy as np

class NeuralNetwork:
    """
    A class to represent the brain of the player/user.

    Attributes
    ----------
    input_nodes : int
        number of input nodes
    hidden_nodes : int
        number of hidden nodes
    output_nodes : int
        number of output nodes
    input_hidden_weights : numpy.array
        the weights between the input nodes and the hidden nodes
    hidden_output_weights : numpy.array
        the weights between the hidden nodes and the output nodes
    hidden_bias : numpy.array
        the bias for the hidden weights
    output_bias : numpy.array
        the bias for the output weights

    Methods
    -------
    sigmoid(x_var:int):
        Activation function to normalize the output data.
    predict(input_values:list):
        Given the input values, predict an action.
    """
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        # Create node counts
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Create weights with random values to start with
        self.input_hidden_weights = np.random.rand(self.hidden_nodes, self.input_nodes)
        self.hidden_output_weights = np.random.rand(self.output_nodes, self.hidden_nodes)

        # Create biases
        self.hidden_bias = np.random.rand(self.hidden_nodes, 1)
        self.output_bias = np.random.rand(self.output_nodes, 1)

    def sigmoid(self, x_var):
        '''
        Activation function to normalize the output information.

                Parameters:
                        x_var (float): The number in the sigmoid function
                Returns:
                        a (float): Resulting calculation of the sigmoid function
        '''
        return 1 / (1 + math.exp(-x_var))

    def predict(self, input_values):
        '''
        Predicts an action based on the given input values.

                Parameters:
                        input_values (list): The input values to calculate from
                Returns:
                        output (list): List of the resulting predictions
        '''
        # Vectorize the sigmoid function
        sigmoid_v = np.vectorize(self.sigmoid)

        # Calculate the hidden layer using inputs
        inputs = np.asanyarray(input_values)
        hidden = np.multiply(self.input_hidden_weights, inputs)

        # Normalize the hidden data
        hidden = np.add(hidden, self.hidden_bias)
        hidden = sigmoid_v(hidden)

        # Calculate the output layer using hidden layer
        output = np.multiply(self.hidden_output_weights, hidden)

        # Normalize the data and return
        output = np.add(output, self.output_bias)
        output = sigmoid_v(output)

        return output.tolist()
