import time
from nltk.tokenize import word_tokenize
import re
import math
import sys
import glob
import pickle
from collections import defaultdict


class Predictor:
    '''
    Predictor which will do prediction on emails
    '''
    def __init__(self, spamFolder, hamFolder):
        self.__createdAt = time.strftime("%d %b %H:%M:%S", time.gmtime())
        self.__spamFolder = spamFolder
        self.__hamFolder = hamFolder
        # do training on spam and ham
        self.__train__()

    def __train__(self):
        '''train model on spam and ham'''
        # Set up the vocabulary for all files in the training set
        vocab = defaultdict(int)
        print "Training Spam"
        vocab.update(self.files2countdict(glob.glob(self.__spamFolder+"/*")))
        print "Training Ham"
        vocab.update(self.files2countdict(glob.glob(self.__hamFolder+"/*")))
        # Set all counts to 0
        vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))

        self.classes = []

        for dir in [(True, self.__spamFolder), (False, self.__hamFolder)]:
            # Initialize to zero counts
            countdict = defaultdict(int, vocab)
            # Add in counts from this class
            countdict.update(self.files2countdict(glob.glob(dir[1]+"/*")))

            total = 0
            for count in countdict.values():
                total = total+count
            # the extra 1 comes from the insertion of an 'unknown' word
            total = float(total + len(countdict)) + 1

            for word in countdict:
                countdict[word] = (countdict[word] + 1) / total
            # this will be called for any unseen word
            countdict['***UNKNOWN***'] = 1/total

            self.classes.append((dir[0],countdict))

    def predict(self, filename):
        '''Take in a filename, return whether this file is spam
        return value:
        True - filename is spam
        False - filename is not spam (is ham)
        '''
        answers = []
        countdict = self.files2countdict([filename])
        for c in self.classes:
            logp = 0
            for word in countdict:
                #for each word, find the probability that it would appear in c
                prob = c[1][word];
                if prob == 0:
                    prob = c[1]["***UNKNOWN***"]
                logp = logp + math.log10(prob)

            answers.append((logp,c[0]))
        answers.sort()
        return answers[1][1]

    def files2countdict (self, files):
        """Given an array of filenames, return a dictionary with keys
        being the space-separated, lower-cased words, and the values being
        the number of times that word occurred in the files."""
        d = defaultdict(int)
        for file in files:
            #skip everything until the first empty line
            #header=False
            for word in word_tokenize(open(file).read()):
            #for line in open(file).read():
                #if header:
                    #for word in line.split():
                        d[self.getWordCase(word)] += 1
                #else:
                #    if line.strip() == "":
                #        header=True
            #if header==False:
            #    print file
        return d

    def getWordCase (self, word):
        # all upper or something else
        # all lower case or title
        for c in word[1:]:
            if c.isupper():
                return word.upper()
        return word.lower()
