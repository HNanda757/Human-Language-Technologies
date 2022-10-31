# By: Harshith Nanda and Charith Muppidi

import nltk
import pickle


def probability(text, unigram_dict, bigram_dict, v):  # calculates laplace probability
    tokens = nltk.word_tokenize(text)
    bigrams = list(nltk.ngrams(tokens, 2))  # creates a list of bigrams
    laplace = 1
    for i in bigrams:
        b = bigram_dict["".join(i)] if "".join(i) in bigram_dict else 0
        u = unigram_dict[i[0]] if i[0] in unigram_dict else 0
        laplace = laplace * ((b + 1) / (u + v))
    return laplace


if __name__ == '__main__':
    english_unigrams = pickle.load(open('english_unigrams.pickle', 'rb'))  # Unpickles and loads all files into dicts
    english_bigrams = pickle.load(open('english_bigrams.pickle', 'rb'))
    french_unigrams = pickle.load(open('french_unigrams.pickle', 'rb'))
    french_bigrams = pickle.load(open('french_bigrams.pickle', 'rb'))
    italian_unigrams = pickle.load(open('italian_unigrams.pickle', 'rb'))
    italian_bigrams = pickle.load(open('italian_bigrams.pickle', 'rb'))
    v = len(english_unigrams) + len(french_unigrams) + len(italian_unigrams)

    with open('LangId.test', 'r') as f:  # opens test file
        test = f.readlines()

    testfile = open('testfile.txt', 'w+') # creates new output file
    for i in test:
        english = probability(i, english_unigrams, english_bigrams, v)  # calls probability for each language
        french = probability(i, french_unigrams, french_bigrams, v)
        italian = probability(i, italian_unigrams, italian_bigrams, v)
        if (english < french) and (english < italian):  # compares probabilities and prints the correct language
            testfile.write('English\n')
            print('English:', english)
        elif (french < english) and (french < italian):
            testfile.write('French\n')
            print('French:', french)
        else:
            testfile.write('Italian\n')
            print('Italian:', italian)
    testfile.close()

    with open('testfile.txt', 'r') as f: # reopens output file
        temp = f.readlines()

    with open('LangId.sol', 'r') as f:  # opens solutions
        solutions = f.readlines()

    count = 0
    idx = []
    for i in range(len(solutions)):  # Prints accuracy and incorrect lines
        t = solutions[i].split(' ')
        if t[1] == temp[i]:
            count += 1
        else:
            idx.append(i)
    accuracy = count / 300
    print('Accuracy:', accuracy)  # This program yields accuracy of 0.9 or 90%
    print('Incorrect line numbers:')
    print(*idx, sep=", ")
