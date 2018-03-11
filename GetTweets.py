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
    # consumer_key = "nFu2HqrelkEiax0L5Lh4Sw"
    consumer_key = "2yIo9afkmT8nDRhuwAdPvwXuR"
    # consumer_secret = "6OUaIfj0ECfeJD24CVlDrcc1qqajnHBgsB7b6RPmvA"
    consumer_secret = "DHh9B4En6yJgDi9UrIy7433gR33qEUIY8bQOmDosC5Wnwb0fCb"
    # access_token = "1193875656-G3iatRJ18tCCFTf8x06kV5B6XwdWbja4S4DVXDL"
    access_token = "1397640175-YXE7NKebRp1h64UTd1sJu7hhsEtgsU9y4s9yW6b"
    # access_token_secret = "IGOxuEQYeTREpGkL4F5LkdYNxUPLFo0zBjX3Yfdg8g"
    access_token_secret = "Fztu1fZQDABGT5QFR8Ss4T5AlcGC14PPxc9BtgKGKwoBb"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print ("Establishing stream...\n")
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener(maxnum=0))

    setTerms = ['bottleneck', 'block', 'congestion', 'blockage', 'delay', 'jam', 'rush', 'traffic', 'stoppage', 'backup',
                'hindrance', 'problem', 'logjam', 'line', 'roadblock', 'deadlock', 'obstruction', 'slow', 'queue',
                'gridlock', 'slow', 'accident', 'crash', 'crowd']
    print ('1')
    sapi.filter(None, setTerms, locations=[68.14712,23.63936,97.34466,28.20453], languages=["en"])
    print('2')



if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print ("Disconnecting from Twitter... ",)
        print ("Done")




