# Make tensorflow shut up about using CPU instructions.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import math, random

import numpy as np

from keras.layers import *
from keras.models import *
from keras.optimizers import *

import data

def new_model():
    charset = data.get_char_corpus()

    model = Sequential();
    
    model.add(Embedding(len(charset)+1, 1+int(2+math.sqrt(len(charset))), input_length=None))

    model.add(LSTM(len(charset) + 1))
    model.add(Dense(len(charset) + 1))
    model.add(Activation('softmax'))

    model.compile(optimizer=Adadelta(), loss='binary_crossentropy')
    
    print('input_shape:', model.input_shape)

    return model

def save(model, name='model.h5'):
    model.save(name)

def load(name='model.h5'):
    return load_model(name) if os.path.isfile(name) else None

def reset(name='model.h5'):
    # Destroy the model
    if os.path.isfile(name):
        os.remove(name)

def respond_to(model, x, max_len=100):
    charset = data.get_char_corpus()

    pt = data.str_to_arr(x)
    s = ''
    
    # Use the model to build the string
    for _ in range(max_len):
        y = model.predict(np.array([pt]))[0]

        #idx = np.argmax(y)
        #idx = np.random.choice(len(y), p=y)
        idx = -1
        while idx < 0 or y[idx] < 1. / len(y):
            idx = np.random.choice(len(y), p=y)
        #print(charset[idx], ':', y[idx])

        pt.append(idx)
        if idx == len(charset):
            break # End when a null terminator is given
        else:
            s += charset[idx]
    
    return s

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help='model filename', default='model.h5', type=str)
    parser.add_argument('-i', '--input', help='input string', default='', type=str)

    args = parser.parse_args()

    # Get the model
    model = load(args.model)

    if model is None:
        # The model was bad
        print("It seems my neural net has been stolen.")
        exit()
    
    # Generate input string
    x = ''.join(filter(lambda x: x in data.get_char_corpus(), args.input))

    # Generate output string
    try:
        y = respond_to(model, x)
        print(y)
    except:
        print("It seems my neural net is malfunctioning.")

