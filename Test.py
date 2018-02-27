class Test ():
    def __init__(self, classifier, extract_features):
        self.classifier = classifier
        self.features = extract_features

def Test(classifier, extract_features):
    var = ''
    while (var != 'exit'):
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