import numpy as np
import scipy.special
from config import *


class Nnet:
    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.weight_input_hidden = np.random.uniform(
            -0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.weight_hidden_output = np.random.uniform(
            -0.5, 0.5, size=(self.num_output, self.num_hidden))
        self.activation_fun = lambda x: scipy.special.expit(x)

    def get_outputs(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        hidden_inputs = np.dot(self.weight_input_hidden, inputs)
        hidden_outputs = self.activation_fun(hidden_inputs)
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
        final_outputs = self.activation_fun(final_inputs)
        return final_outputs

    def get_max_value(self, inputs_list):
        outputs = self.get_outputs(inputs_list)
        return np.max(outputs)

    def modify_weights(self):
        Nnet.modify_arr(self.weight_hidden_output)
        Nnet.modify_arr(self.weight_input_hidden)

    def create_mixed_weights(self, net1, net2):
        self.weight_input_hidden = Nnet.mix_arr(
            net1.weight_input_hidden, net2.weight_input_hidden)
        self.weight_hidden_output = Nnet.mix_arr(
            net1.weight_hidden_output, net2.weight_hidden_output)

    def modify_arr(arr):
        for x in np.nditer(arr, op_flags=['readwrite']):
            if np.random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def mix_arr(arr1, arr2):
        if arr1.size == arr2.size:
            entries_lenght = arr1.size
            num_rows = arr1.shape[0]
            num_cols = arr1.shape[1]

            no_mutate = entries_lenght - \
                int(entries_lenght * MUTATION_ARRAY_MIX_PEC)
            idx = np.random.choice(
                np.arange(entries_lenght), no_mutate, replace=False)
                
            res = np.random.rand(num_rows, num_cols)

            for row in range(0, num_rows):
                for col in range(0, num_cols):
                    index = row * num_cols + col
                    if index in idx:
                        res[row][col] = arr1[row][col]
                    else:
                        res[row][col] = arr2[row][col]
            return res

        else:
            raise Exception('arrays are of different length!')


def test():
    arr1 = np.random.uniform(-0.5, 0.5, size=(3, 4))
    arr2 = np.random.uniform(-0.5, 0.5, size=(3, 4))

    print('arr1', arr1, sep='\n')
    print('arr2', arr2, sep='\n')

    Nnet.modify_arr(arr1)
    print('arr1_MODIFIED', arr1, sep='\n')

    mixed = Nnet.mix_arr(arr1, arr2)
    print('mixed', mixed, sep='\n')


if __name__ == '__main__':
    test()
