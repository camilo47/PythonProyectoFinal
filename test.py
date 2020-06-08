# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:46:20 2020

@author: kmisk
"""
import pandas as pd
import numpy as np

from sklearn.neural_network import MLPRegressor

#datos = pd.read_csv('text_pred.csv')
datos = pd.read_csv('data.txt',parse_dates = ['fecha'])


print(datos)
x = datos['fecha']
y = datos['dia']

X = x[:,np.newaxis]



while True:
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    mlr = MLPRegressor(solver = 'sgd', alpha=1e-15, hidden_layer_sizes=(12,3), random_state = 1)
    mlr.fit(X_train, y_train)
    print(mlr.score(X_train, y_train))
    if mlr.score(X_train, y_train) > 0.9:
        break

print('Predict to ', mlr.predict('2020-01-01'))