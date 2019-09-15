import sys
import datetime
import tweepy
import pandas as pd
from pandas import DataFrame

# Copy and paste your 4 security keys from the identification.txt file
consumer_key = "6AdhuV53cBqZUfAbfyI9jjDPi"
consumer_secret = "4FmqlhbGOSDuDhonlBnxXwiIlbUllmMNEvy9FLQ09e05DgUatP"
access_token = "1143956300155510785-YLi7RbXUwoP6fPDWSa4QcusjtL2DBc"
access_token_secret = "aOLXmhbejnAFD6pdyo0fDU2cfPA07jRhNUScha8UJ9Xpa"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# ***** Create the pandas data frame to store your twitter data with columns of user, tweet, location and time ******
df = pd.DataFrame(columns=['tweet', 'user', 'Coord_x', 'Coord_y', "date", "time"])
# Number of total tweets you wish to get from the live twitter stream
search_number = 300


class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super(CustomStreamListener, self).__init__()
        self.num_tweets = 0

    def on_status(self, status):
        global df
        try:
            # 1. Get all of our data from tweets
            user = status.user.screen_name
            tweet = status.text
            coord_x = status.coordinates['coordinates'][0]
            coord_y = status.coordinates['coordinates'][1]
            date_utc = status.created_at
            h_m_s_utc = (str(status.created_at.hour)) + ':' + (str(status.created_at.minute)) + ':' + (str(status.created_at.second))
            date_est = datetime.datetime.now()
            h_m_s_est = (str(date_est.hour)) + ':' + (str(date_est.minute)) + ':' + (str(date_est.second))

            # ***** Save your data to a Pandas Series (list) to append to our data frame*****
            save = pd.Series([tweet, user, coord_x, coord_y, date_est, h_m_s_est],
                             index=['tweet', 'user', 'Coord_x', 'Coord_y', "date", "time"])

            df = df.append(save, ignore_index=True)

            # Print the user and associated tweet to see the current twitter stream
            print(user)
            print(tweet)
            self.num_tweets += 1

            # If statement for stopping the twitter stream when you reach the desired number of tweets
            if self.num_tweets < search_number:
                return True
            else:
                return False

        except:
            # If there are no coordinates for a tweet, then pass
            pass

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True  # Don't kill the stream


# ----------------Script execution----------------
listener = tweepy.streaming.Stream(auth, CustomStreamListener())
print("Looking for tweets...")

# Change the values to track what you have chosen to map
listener.filter(track=[' #pride','#gay', '#happypridemonth', '#pride2019','#pridemonth2019', '#pridemonth', '#prideparade', '#pride', '#gaypride', '#loveislove', '#lgbtpride', '#queerpride', '#gaysummer', 'queer', 'queerpride', 'lgbt', 'lgbti', 'lgbtq', 'igbtsupporter'])

#*****Save your dataframe to a csv file*****
df.to_csv('C:/geog 381/a03_tweet/data_nyc.csv', encoding="utf-8")
print("Tweet data frame successfully saved!")


