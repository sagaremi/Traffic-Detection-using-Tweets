import sys
import tweepy, csv
import re
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import io
from CleanTweets import clean

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, maxnum, api=None):
        self.n = maxnum
        self.api = api

    def on_status(self, status):
        #print (status.text)
        try:
            tweets = []
            name = status.author.screen_name
            textTwitter = status.text

            final_tweet = clean(textTwitter)

            gooddata = open('dataset.csv', 'ab+')
            writer = csv.writer(gooddata)
            temp = []
            temp.append(final_tweet)
            print final_tweet
            writer.writerow(temp)


            self.n = self.n + 1
            if self.n < 3000:
                return True
            else:
                print ('maxnum = ' + str(self.n))
                return False

        except Exception as e:
            print (e)

    def on_error(self, status_code):
        # print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        # print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


    def on_error(self, status_code):
        # print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        # print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream



def main():
    print ('in main.....')
    consumer_key = "nFu2HqrelkEiax0L5Lh4Sw"
    consumer_secret = "6OUaIfj0ECfeJD24CVlDrcc1qqajnHBgsB7b6RPmvA"
    access_token = "1193875656-G3iatRJ18tCCFTf8x06kV5B6XwdWbja4S4DVXDL"
    access_token_secret = "IGOxuEQYeTREpGkL4F5LkdYNxUPLFo0zBjX3Yfdg8g"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print ("Establishing stream...\n")
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener(maxnum=0))

    setTerms = ['bottleneck', 'block', 'delay', 'excess', 'congestion', 'blockage', 'delayline', 'jam', 'rush', 'hour',
                'traffic', 'stoppage', 'backup', 'snarl-up', 'hindrance', 'entanglement', 'holdup', 'problem',
                'mobbing', 'logjam', 'line', 'roadblock', 'deadlock', 'stalemate', 'obstruction', 'cramming',
                'stagnation', '1and', 'slow', 'down', 'log-jam', 'queue', 'gridlock', 'slow-up', 'tie-up', 'tailback',
                'accident', 'crash', 'crowd']
    print ('1')
    sapi.filter(None, setTerms, locations=[68.14712,23.63936,97.34466,28.20453], languages=["en"])
    print('2')



if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print ("Disconnecting from Twitter... ",)
        print ("Done")




