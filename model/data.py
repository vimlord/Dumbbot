
from functools import *
import random

import os

import numpy as np

import pickle

datapath = '.'

def set_datapath(path):
    global datapath
    datapath = path

def strip_movie_line(line):
    # Get the line id
    i = line.index(' ')
    lineId = line[:i]
    line = line[i+1:]
    
    for _ in range(7):
        line = line[line.index(' ')+1:]

    line = ''.join(c for c in line if ord(c) < 128)

    return {'idx' : int(lineId[1:]), 'text' : line}

def strip_movie_conv(line):
    for _ in range(6):
        line = line[line.index(' ')+1:]

    res = eval(line)
    return list(map(lambda x: int(x[1:]), res))
    
line_corpus = None
convs = None
char_corpus = None

def load_dataset():
    global line_corpus
    global convs

    cName = os.path.join(datapath, 'convs.pkl')
    lName = os.path.join(datapath, 'lines.pkl')
    if os.path.isfile(cName) and os.path.isfile(lName):
        with open(cName, 'rb') as f:
            convs = pickle.load(f)
        with open(lName, 'rb') as f:
            line_corpus = pickle.load(f)
        
        print('Loaded', len(line_corpus), 'lines of dialog across', len(convs), 'conversations')

    else:
        process_dataset()
        

def process_dataset():
    global line_corpus
    global char_corpus
    global convs

    global datapath
    
    print('Extracting movie lines')
    lines = [line.rstrip('\n') for line in open(os.path.join(datapath, 'movie_lines.txt'), encoding="ISO-8859-1")]
    lines = list(map(strip_movie_line, lines))
    print('Found', len(lines), 'movie lines')
    
    # Filter the lines
    lines = list(filter(lambda x: len(x['text']) < 120, lines))
    print('Trimmed to', len(lines), 'movie lines')
    
    print('Building corpuses')
    chars = set()
    line_corpus = {}
    for line in lines:
        txt = line['text']
        idx = line['idx']
        
        # Build the charset
        for c in txt:
            if c not in chars:
                chars.add(c)

        line_corpus[idx] = line['text']
    
    print('Saving line corpus')
    with open(os.path.join(datapath, 'lines.pkl'), 'wb') as f:
        pickle.dump(line_corpus, f, pickle.HIGHEST_PROTOCOL)
    
    # Convert to a string
    char_corpus = reduce(lambda x,y: x+y, sorted(chars), '')

    # Save the charset if it does not yet exist
    print('Saving charset')
    if not os.path.isfile('charset.txt'):
        with open('charset.txt', 'w') as f:
            f.write(char_corpus)

    print('charset:', char_corpus)

    print('Extracting movie conversations')
    convs = [line.rstrip('\n') for line in open(os.path.join(datapath, 'movie_conversations.txt'), encoding="ISO-8859-1")]
    convs = list(map(strip_movie_conv, convs))
    print('Found', len(convs), 'conversations')

    # Filter for the valid conversations
    convs = list(filter(lambda c: all(x in line_corpus for x in c), convs))
    print('Trimmed to', len(convs), 'conversations')

    print('Saving conversation mappings')
    with open(os.path.join(datapath, 'convs.pkl'), 'wb') as f:
        pickle.dump(convs, f, pickle.HIGHEST_PROTOCOL)


def str_to_arr(s):
    global char_corpus

    pt = []
    for c in s:
        pt.append(char_corpus.index(c))
    pt.append(len(char_corpus))

    return pt

def gen_conv_corpus(k = None, verbose=True):
    global convs
    global line_corpus

    # If the conversation set is unavailable, generate the corpus
    if not convs:
        if verbose: print('The coversation corpus is not present. Initializing dataset...')
        load_dataset()

    # Grab k conversations
    convos = random.sample(convs, k) if k != None else convs

    data = []

    for conv in convos:
        for i in range(len(conv)-1):
            a, b = line_corpus[conv[i]], line_corpus[conv[i+1]]
            pt = str_to_arr(a) + str_to_arr(b)
            
            # Add the point
            data.append(pt)

    return data

def get_char_corpus():
    global char_corpus

    if not char_corpus:
        # If the character set is not yet built, we should acquire it.
        if os.path.isfile('charset.txt'):        
            # Read it from the file
            with open('charset.txt', 'r') as f:
                char_corpus = reduce(lambda x,y: x+y, sorted(f.read()), '')
        else:
            print('The char corpus is not present. Initializing dataset...')
            # Load the dataset to get the charset
            process_dataset()

    return char_corpus

char_corpus = None

if __name__ == '__main__':
    for l in line_corpus:
        print(str(l) + " : " + line_corpus[l])

    for c in convs:
        print(c)

    print(char_corpus)
    print('Char count:', len(char_corpus))
    print('Conversation count:', len(convs))
    print('Line pairing count:', sum([len(c) for c in convs]) - len(convs))

