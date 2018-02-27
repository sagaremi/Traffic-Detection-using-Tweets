import sys
import csv
import tweepy
import re
import nltk
import string
from nltk.classify import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.corpus import stopwords
import nltk.classify.util
from Test import Test


def featureExtraction():
    inpTweets = csv.reader(open('dataset.csv', 'rb'), delimiter=',', quotechar=' ')
    tweets = []

    for rowTweet in inpTweets:
        label = rowTweet[1]
        tweet = rowTweet[0]
        featureVector = getFeatureVector(tweet)
        tweets.append((featureVector, label))
    return tweets  # Here I am returning the tweets inside the array plus its sentiment


def getFeatureVector(tweet):
    featureVector = []
    # split tweet into words
    words = tweet.split()
    for w in words:
        w = replaceTwoOrMore(w)  # replace two or more with two occurrences
        w = w.strip('\'"?,.')  # strip punctuation
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)  # check if the word starts with an alphabet
        if (w in stopWords or val is None):  # ignore if it is a stop word
            continue
        else:
            featureVector.append(w.lower())
    return featureVector


def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def getStopWordList(stopWordListFileName):
    stopWords = []

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords


def get_words_in_tweets(tweets):
    all_words = []
    for (text, sentiment) in tweets:
        all_words.extend(text)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)  # This line calculates the frequency distrubtion of all words in tweets
    word_features = wordlist.keys()  # This prints out the list of all distinct words in the text in order
    # of their number of occurrences.
    return word_features


def extract_features(tweet):
    settweet = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in settweet)
    return features


stopWords = getStopWordList('StopWords.txt')
tweets = featureExtraction()
word_features = get_word_features(get_words_in_tweets(tweets))  # my list of many words

# extract feature vector for all tweets in one shot
training_set = nltk.classify.apply_features(extract_features, tweets[:-250])
test_set = nltk.classify.apply_features(extract_features, tweets[-250:])

# ****** Naive Bayes Classifier******************************************

classifier = nltk.NaiveBayesClassifier.train(training_set)

accuracy = nltk.classify.accuracy(classifier, training_set)
print (accuracy)

total = accuracy * 100
print ('Naive Bayes Accuracy: %4.2f' % total)

# Accuracy Test Set
accuracyTestSet = nltk.classify.accuracy(classifier, test_set)
print (accuracyTestSet)

totalTest = accuracyTestSet * 100
print ('\nNaive Bayes Accuracy with the Test Set: %4.2f' % totalTest)

print ('\nInformative features')
print (classifier.show_most_informative_features(n=15))
# **************************



var = ''
while (var != 'exit'):
    try:
        input = input('\nPlease write a sentence to be tested sentiment. If you type - exit- the program will exit \n')
        print ('\n')
        if input == 'exit':
            print ('Exiting the program')
            var = 'exit'
            # break
        else:
            input = input.lower()
            input = input.split()

            print ('\nNaive Bayes Classifier')
            print (
            'I think that the sentiment was ' + classifier.classify(extract_features(input)) + ' in that sentence.\n')
    except Exception as e:
        print e
        continue



