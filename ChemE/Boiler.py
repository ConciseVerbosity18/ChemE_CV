from scipy.optimize import fsolve, curve_fit
from numpy import log as ln
from scipy.integrate import odeint, quad
import numpy as np
from numpy import sin,cos,tan
from numpy import sinh, cosh,tanh
from numpy import pi
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
import pandas as pd
from scipy.special import erf,erfc,erfinv,erfcinv

def paste_to_df(s:str,sep=' ',rows=True,rowsplit='\n'):
    df = pd.DataFrame()
    if not rows:
        s = s.split(sep)
        df[1] = s
    else:
        s = s.split(rowsplit)
        s = list(map(lambda x: x.split(sep),s))
        ml = 0
        for row in s:
            ml = len(row) if len(row) > ml else ml
        for i, row in enumerate(s):
            while len(row)<ml:
                row.append(np.NaN)
            df[f'{i}'] = row
    return df
if __name__== '__main__':
    print(paste_to_df('204.9, 206.1, 203.9, 207.0, 203.5, 206.3, 203.5, 206.7, 205.8\n1.317, 1.318, 1.301, 1.307, 1.374, 1.323',', '))