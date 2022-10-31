# By: Harshith Nanda and Charith Muppidi

import nltk
import pickle


def createDict(list):  # creates dictionary without using count() to make it faster
    dict = {}          # using count() is n^2 time, so it takes over 3 minutes to run
    for i in list:     # this method runs in a few seconds
        n = " ".join(i)
        if n in dict:
            dict[n] += 1
        else:
            dict[n] = 1
    return dict


def ngrams(filename):
    with open(filename, encoding='utf8') as f:
        text = f.read()  # reads in text
    text = text.strip('\n')  # strips text of newlines
    tokens = nltk.word_tokenize(text)
    bigrams = list(nltk.ngrams(tokens, 2))  # creates a list of bigrams
    unigrams = list(nltk.ngrams(tokens, 1))  # creates a list of unigrams
    num_unigrams = createDict(unigrams)
    num_bigrams = createDict(bigrams)
    return num_unigrams, num_bigrams


if __name__ == '__main__':
    print("English")
    english_unigrams, english_bigrams = ngrams('LangId.train.English')  # calls function for each language file
    print("French")
    french_unigrams, french_bigrams = ngrams('LangId.train.French')
    print("Italian")
    italian_unigrams, italian_bigrams = ngrams('LangId.train.Italian')

    with open('english_unigrams.pickle', 'wb') as f:  # creates a pickle dump file for each language dictionary
        pickle.dump(english_unigrams, f)

    with open('english_bigrams.pickle', 'wb') as f:
        pickle.dump(english_bigrams, f)

    with open('french_unigrams.pickle', 'wb') as f:
        pickle.dump(french_unigrams, f)

    with open('french_bigrams.pickle', 'wb') as f:
        pickle.dump(french_bigrams, f)

    with open('italian_unigrams.pickle', 'wb') as f:
        pickle.dump(italian_unigrams, f)

    with open('italian_bigrams.pickle', 'wb') as f:
        pickle.dump(italian_bigrams, f)
