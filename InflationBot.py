import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

data = open('intents.json').read()
intents = json.loads(data)
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('InflationBot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


def _predict_class(sentence):
    p = bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.1
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def _get_response(return_list, intents_json):
    try:
        tag = return_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
    except IndexError:
        result = "I don't understand!"
    return result


print("InflationBot is online!")

users = pickle.load(open('users.pkl', 'rb'))
name = ""
while True:
    name = input("Hello, what's your username? (It doesn't have to be your actual name!)")
    if name in users:
        print("Sorry, that username is already taken. Choose a different name please!")
    else:
        break

print("Thanks, you may ask me whatever you want now!")

file = open("Conversation.txt", "w+")
while True:
    msg = input("")
    file.write(name + ": " + msg + "\n")
    if msg.lower() == 'end':
        break
    ints = _predict_class(msg)
    res = _get_response(ints, intents)
    file.write("Inflation Bot: " + res + "\n")
    print(res)
file.close()
f = open("Conversation.txt", "r")
convo = f.readlines()
users.update({name: convo})
f.close()
pickle.dump(users, open('users.pkl', 'wb'))  # Dict containing users and their conversations is stored
