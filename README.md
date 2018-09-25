
# Dumbbot

## Introduction

Dumbbot is a website-based bot that was written for the September 2018 Codejam
held by the Stevens Computer Science Club. The program is designed around the
theme "parodies" in that it is a parody of [Cleverbot](http://cleverbot.com), a
chatbot that responds to user messages. I have parodied it by training a bot
that also takes in user responses, and yields a response,

The bot is powered by a recurrent neural network that, given a segment of a
conversation, generates the next character of the conversation. By repeating this
operation, the program is capable of generating a response to a given query.

## Requirements

To setup a Dumbbot server on your machine, you will require Python 3 and NodeJS.
You will also need NPM and Pip for installing libraries.

## Installation

First, you will need to download the
[Cornell Movie Dialog Corpus](http://www.cs.cornell.edu/~cristian//Cornell_Movie-Dialogs_Corpus.html).
Once it is downloaded, extract it to a directory of your choice. There should be
some text files inside, notably movie\_lines.txt and movie\_lines.txt. Supposing
the path to these files is /path/to/cornell (ex: movie lines is at /path/to/cornell/movie\_lines.txt),
we wan move on.

Once the requirements are met, you will need to do the following:

```
pip install keras # Keras is a deep learning API
npm install # Initializes the node modules
```

Once this is done, you will need to generate the dataset and train the model.
If you use the training program, this is all handled for you. By default, you
can train the model with:

```
python model/train.py -d /path/to/cornell -t 5000
```

This will run the model for 5000 iteration. During each iteration, a number of
conversations will be processed for sequential movie lines and fed to the model.
The first time the model is run, it may take a while to start. This is because
it will need to generate the processed data. When it is generated, the dataset
will be saved in the same directory as the Cornell dataset as a pair of .pkl files
that contain an encoding of the data. A file charset.txt will also be created
in the current directoy, and is used to map between characters and the input
embedding.

## Usage

To generate text manually, one can run ```python model/model.py -i "Your text here"```.
This command is invoked by the NodeJS server when a request is made.

To run the server, simply run ```npm start```. You can also use ```nodemon app.js```
if you prefer to use ```nodemon```.

By default, the server is hosted on port 80. This can be changed in app.js.

