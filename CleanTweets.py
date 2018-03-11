import re, string, csv
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


stemmer = PorterStemmer()
stop_words = open('StopWords.txt')


def clean(rawtweet):
    try:
        # tokenisation
        punctuationPattern = re.compile('[%s]' % re.escape(string.punctuation))
        pricePattern = re.compile(r"\d+\.\d\d")
        numberPattern = re.compile(r"\d+")
        emoji_pattern = re.compile(u'/(?:\uD801[\uDDC0-\uDFFF]|[\uD802-\uD831][\uDC00-\uDFFF]|\uD832[\uDC00-\uDF40])/',
                                   flags=re.UNICODE)

        tweet = rawtweet.lower()
        tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))', '', tweet)   # remove www.* or https?://* (URL)
        tweet = re.sub('@[^\s]+', '', tweet)                            # remove @username
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)                      # Replace #word with word Handling hashtags
        tweet = re.sub(punctuationPattern, '', tweet)                   # Remove punctuations
        tweet = re.sub(pricePattern, '', tweet)                         # Remove prices
        tweet = re.sub(numberPattern, '', tweet)                        # Remove numbers
        tweet = re.sub(emoji_pattern, '', tweet)                        # Remove emojis
        tweet = tweet.replace('rt', '')                                 # Remove retweet symbol
        tweet = re.sub('[\s]+', ' ', tweet)                             # Remove additional white spaces
        tweet = tweet.strip('\'"').strip()                              # trim
        tweet = tweet.encode('ascii', 'ignore')

        # word_tokens = word_tokenize(tweet)
        # filtered_tweet = [w for w in word_tokens if not w in stop_words]
        # for w in word_tokens:
        #     if w not in stop_words:
        #         filtered_tweet.append(w)

    except Exception as e:
        print e

    # stop word filtering

    return tweet


if __name__ == '__main__':
    try:
        rawdata = open('./Datasets/training_set_tweets.txt', 'r')
        rowcount = 0
        n=0

        gooddata = open('dataset%s.csv' %n, 'wb+')
        writer = csv.writer(gooddata)
        for line in rawdata.readlines():
            if rowcount < 2000:
                line = clean(line)
                writer.writerow(line.split())       #Each pre-processed tweet converted into tokens
                rowcount += 1
            else:
                gooddata.close()
                print n
                n += 1
                rowcount = 0
                gooddata = open('dataset%s.csv' % n, 'wt')
                writer = csv.writer(gooddata)
                line = clean(line)
                writer.writerow(line.split())
                rowcount += 1

        gooddata.close()
        rawdata.close()


    except Exception as e:
        print (e)