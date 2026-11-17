from keras.layers import Dense, Dropout, Input
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

from sentence_transformers import SentenceTransformer

import random as rn
import numpy as np
import pickle as pk
import json

JSON_PATH = "../json/resume.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"   # یا مدل چندزبانه اگر فارسی هم لازم داری

# load json file
def load_intents(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

#  load and read data
def prepare_data(intents_file):
    classes = []
    documents = []
    sentences = []
    labels = []

    for intent in intents_file['intents']:
        for pattern in intent['patterns']:
            #add documents in the corpus
            documents.append((pattern, intent['tag']))
            sentences.append(pattern)
            labels.append(intent['tag'])
            # add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # Database Preparation
    #  sort classes
    classes = sorted(list(set(classes)))
    #  documents = combination between patterns and intents
    print(len(documents), "documents")
    # classes = intents
    print(len(classes), "classes")

    #  Data science store
    pk.dump(classes, open('../pkl/classes.pkl', 'wb'))

    return sentences, labels, classes


# creat our training data
def build_training_data(sentences, labels, classes):
    # (new) sentence embedding instead of bag of words
    encoder = SentenceTransformer(MODEL_NAME)
    train_X = encoder.encode(sentences, normalize_embeddings=True)
    print("embedding shape:", train_X.shape)

    # creater an empty array for our output
    # output is a '0' for each tag and '1' for current tag (for each patttern)
    train_Y = np.zeros((len(sentences), len(classes)), dtype="float32")
    for i, tag in enumerate(labels):
        train_Y[i, classes.index(tag)] = 1

    # shuffle our features and turn into np.array
    indices = np.arange(len(sentences))
    rn.shuffle(indices)
    train_X = train_X[indices]
    train_Y = train_Y[indices]

    print('Training data created')
    return train_X, train_Y


# create model - 3 layers. first layer 128 neurons, second layer 64 neurons 3 output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
def build_model(input_size, output_size):
    model = Sequential([
        Input(shape=(input_size,)),
        Dense(128, activation='relu'),
        Dropout(0.4),
        Dense(64, activation='relu'),
        Dropout(0.4),
        Dense(output_size, activation='softmax'),
    ])

    #  compile model. Stochastic gradint descent with Nesterov accelerated gradient gived good result this model
    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
    return model


# fitting and saving the model
def train_and_save(model, train_X, train_Y):
    earlystop = EarlyStopping(monitor='loss', patience=20, restore_best_weights=True)
    h = model.fit(train_X, train_Y, epochs=500, batch_size=5, callbacks=[earlystop], verbose=1)
    model.save('../model/chatbot_model.keras')
    return h

# main file for load app
def main():
    intents_file = load_intents(JSON_PATH)
    sentences, labels, classes = prepare_data(intents_file)
    train_X, train_Y = build_training_data(sentences, labels, classes)
    model = build_model(train_X.shape[1], len(classes))
    train_and_save(model, train_X, train_Y)
    print('model created')

#  code runner
if __name__ == "__main__":
    main()

print("ok")