import numpy as np
import pandas as pd
# from ChemE.Boiler import *
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import *
from sklearn.metrics import confusion_matrix as confma
from pandas_profiling import ProfileReport as prr
import seaborn as sns
from matplotlib import cm
from sklearn.model_selection import train_test_split as tts
import time
from sklearn.linear_model import LogisticRegression as skLR
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from gekko import GEKKO