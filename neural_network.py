import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

lemmatizer = WordNetLemmatizer()

words = []
classes = []
documents = []
ignore = ['?', '!', ',', '.', "'s"]

data = open('intents.json').read()
intents = json.loads(data)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
users = {"qwwwer": ["Random Convo"], "ran": ["Random Convo"], "rando": ["Random Convo"], "random": ["Random Convo"]}
pickle.dump(users, open('users.pkl', 'wb'))

# pre-processing
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern = doc[0]
    pattern = [lemmatizer.lemmatize(word.lower()) for word in pattern]
    for word in words:
        if word in pattern:
            bag.append(1)
        else:
            bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)
X_train = list(training[:, 0])
y_train = list(training[:, 1])

# Building the Keras sequential model
model = Sequential()
model.add(Dense(128, activation='sigmoid', input_shape=(len(X_train[0]),)))
model.add(Dropout(0.5))
model.add(Dense(64, activation='sigmoid'))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))
# Defining the optimizer, training, and saving the model
adam = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
hist = model.fit(np.array(X_train), np.array(y_train), epochs=430, batch_size=5, verbose=1)
model.save('InflationBot_model.h5', hist)

print('Finished Training')
