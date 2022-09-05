# Process CSV file
# CS 4395 Homework 1
# Harshith Nanda
import sys
import pickle
import re
import pathlib



class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee ID: " + self.id + '\n')
        print(self.first + ' ' + self.mi + ' ' + self.last + '\n')
        print(self.phone, '\n')

if __name__ == '__main__':
    if len(sys.argv) < 2: # File path code taken from github: https://github.com/kjmazidi/NLP/blob/master/Xtra_Python_Material/path%20demo/path_demo.py
        print('Please enter a filename as a system arg')
        quit()

    file = open(pathlib.Path.cwd().joinpath(sys.argv[1]), 'r')
    line = file.readline()

    dictionary = {}

    while True:
        line = file.readline().strip()
        if not line:
            break
        person = line.split(',')

        if len(person[2]) != 1:
            person[2] = 'X'

        while re.match('[A-Z][A-Z][0-9][0-9][0-9][0-9]', person[3]) is None:
            print('ID invalid: ', person[3])
            person[3] = input('Enter an ID: ')

        while re.match('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]', person[4]) is None:
            print(person[4], ' is invalid')
            person[4] = input('Enter phone number: ')

        tempPerson = Person(person[0], person[1], person[2].capitalize(), person[3], person[4])
        dictionary[person[3]] = tempPerson

    # from github: https://github.com/kjmazidi/NLP/blob/master/Xtra_Python_Material/pickle.ipynb
    pickle.dump(dictionary, open('dict.p', 'wb'))
    pickleFile = pickle.load(open('dict.p', 'rb'))
    print('Employee list:' + '\n')
    for num in pickleFile.keys():
        pickleFile[num].display()