"""
A module that consists of a neural network that can make predictions given inputs.

Author
----------
Adam Skudlarek

Classes
----------
NeuralNetwork:
    Makes predictions based off of input.

Functions
----------
sigmoid(x_var:float):
    Activation function to normalize the output information.
mutate_rate(x_var:float):
    Tweaks a given value slightly at a 10% chance rate.

"""
import math
import random
import numpy as np


def sigmoid(x_var):
    '''
    Activation function to normalize the output information.

            Parameters:
                    x_var (float): The number in the sigmoid function
            Returns:
                    a (float): Resulting calculation of the sigmoid function
    '''
    return 1 / (1 + math.exp(-x_var))

def mutate_rate(x_var):
    '''
    There is a 10% chance the given value is teaked slightly.

        Parameters:
                x_var (float): Value to tweak or leave the same
        Returns:
                x (float): Either tweaked value of x_var or the same x_var
    '''
    if random.random() < 0.1:
        offset = random.gauss(0, 1) * 0.5
        new_x = x_var + offset
        return new_x
    else:
        return x_var

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
    predict(input_values:list):
        Given the input values, predict an action.
    copy():
        Returns a Neural Network identical to this one.
    mutate()
        Tweaks the values of all the Neural Network data.
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

    def predict(self, input_values):
        '''
        Predicts an action based on the given input values.

                Parameters:
                        input_values (list): The input values to calculate from
                Returns:
                        output (list): List of the resulting predictions
        '''
        # Vectorize the sigmoid function
        sigmoid_v = np.vectorize(sigmoid)

        # Calculate the hidden layer using inputs
        inputs = np.asanyarray(input_values)
        hidden = np.dot(self.input_hidden_weights, inputs)

        # Normalize the hidden data
        hidden = np.add(hidden, self.hidden_bias)
        hidden = sigmoid_v(hidden)

        # Calculate the output layer using hidden layer
        output = np.dot(self.hidden_output_weights, hidden)

        # Normalize the data and return
        output = np.add(output, self.output_bias)
        output = sigmoid_v(output)

        return output.tolist()

    def copy(self):
        '''
        Returns a copy of itself.

            Returns:
                    copy_of_self (NeuralNetwork): Copy of all of its data
        '''
        # Copy values of nodes
        copy_of_self = NeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)

        # Copy value of weights
        copy_of_self.input_hidden_weights = self.input_hidden_weights
        copy_of_self.hidden_output_weights = self.hidden_output_weights

        # Copy value of biases
        copy_of_self.hidden_bias = self.hidden_bias
        copy_of_self.output_bias = self.output_bias

        # Return copy
        return copy_of_self

    def mutate(self):
        '''
        Mutates all the values of the Neural Network such as weights and biases.
        '''
        # Vectorize the mutation rate
        mutate_rate_v = np.vectorize(mutate_rate)

        # Adjust all weights and biases slightly
        self.input_hidden_weights = mutate_rate_v(self.input_hidden_weights)
        self.hidden_output_weights = mutate_rate_v(self.hidden_output_weights)
        self.hidden_bias = mutate_rate_v(self.hidden_bias)
        self.output_bias = mutate_rate_v(self.output_bias)
