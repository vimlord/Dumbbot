from model import new_model, load, save, reset, respond_to
import data

import numpy as np
from tqdm import tqdm

import argparse, math, random


parser = argparse.ArgumentParser()

parser.add_argument('-d', '--dataset', help='location of training data', type=str, default='.')
parser.add_argument('-m', '--model', help='model filename', default='model.h5', type=str)
parser.add_argument('-t', '--train', help='performs training', default=0, type=int)
parser.add_argument('--sampletext', help='sample input for progress samples', default='Hello there.', type=str)
parser.add_argument('--reset', help='deletes the model before doing anything', action='store_true')

def train(model, epochs=1, batches=1024, sample_input='Hello there.'):
    global model_name
    
    charset = data.get_char_corpus()

    for epoch in range(epochs):
        dataset = data.gen_conv_corpus(batches)
        
        # Generate all of the samples to feed in
        groups = []
        for pt in dataset:
            i = 0
            while pt[i] is not len(charset): i += 1
            i += 1

            while True:
                groups.append(pt[:i+1])

                # Increment if necessary
                if pt[i] is len(charset):
                    break
                else:
                    i += 1
        
        # Shuffle the data
        random.shuffle(groups)
        
        # Group by length. This allows for batching.
        groups = [[p for p in groups if len(p) == length] for length in set([len(x) for x in groups])]
        
        # Rejoin the groups
        dataset = [x for g in groups for x in g]
        
        # Shuffle the groups
        random.shuffle(groups)

        with tqdm(total=sum(map(lambda g: len(g), groups)), unit='pt', desc='iter ' + str(1+epoch)) as pbar:
            for group in groups:
                X, Y = np.array([x[:-1] for x in group]), np.array([[x[-1] == i for i in range(len(charset)+1)] for x in group])
                model.fit(X, Y, epochs=1, verbose=False)

                pbar.update(len(group))
            
        # Generate a sample
        s = sample_input
        print("user:", '"' + s + '"')

        for _ in range(4):
            print("bot:", '"' + respond_to(model, s) + '"')
        
        # Save the model
        save(model, model_name)
        print('Saved model')

if __name__ == '__main__':
    args = parser.parse_args()

    # Provide a dataset location
    data.set_datapath(args.dataset)
    print('Datapath is', args.dataset)

    model_name = args.model

    # Reset on request
    if args.reset:
        print('Deleting existing progress')
        reset(model_name)

    print('Getting char corpus')
    charset = data.get_char_corpus()

    # Attempt to load the model. If that fails, make a new one.
    print('Fetching model')
    model = load(model_name)
    if not model:
        model = new_model()
        print('Generated new model')
    else:
        print('Loaded saved model')

    model.summary()

    if args.train > 0:
        print('Training for', args.train, 'iterations')
        train(model, args.train, sample_input=args.sampletext)


