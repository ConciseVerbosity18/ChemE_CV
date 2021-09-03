import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PID():
    def __init__(self, P,I,D, bias):
        self.P = P
        self.I = I
        self.D = D
        self.bias = bias

    def adjust(self,data:np.array):
        output = self.P*self.prop(data) + self.I*self.inte(data) + self.D*self.der(data) + self.bias

        return output