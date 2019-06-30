"""Provides an interface with the Twitter API"""
from tweepy import API, OAuthHandler
import re


class TwitterClient:
    """Interfaces with the Twitter API"""

    def __init__(self, consumer_key, consumer_secret, access_token,
    access_token_secret):
        """
        Instantiates the TwitterClient and completes authentification with the
        Twitter API

        Parameters
            consumer_key (String): The consumer key
            consumer_secret (String): The consumer secret
            access_token (String): The access token
            access_token_secret (String): The access token secret
        """
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)

    def fetch_tweets(self, user_id):
        """
        Get all visible tweets from the specified user and returns them in a list
        :param user_id:  A unique twitter username
        :return:list(String) A list containing most of the tweets from a user.
        """
        all_tweets = []

        # Max count is 200 tweets, tweet_mode ensures all 280 characters included.
        tweets = self.api.user_timeline(screen_name=user_id, count=200,
            include_rts=False, tweet_mode='extended')

        all_tweets.extend(tweets)
        oldest_id = tweets[-1].id

        # Fetch all tweet's in user's history
        while True:
            tweets = self.api.user_timeline(screen_name=user_id,
                                       # 200 is the maximum allowed count
                                       count=200,
                                       include_rts=False,
                                       max_id=oldest_id - 1,
                                       # Necessary to keep full_text
                                       # otherwise only the first 140 words are extracted
                                       tweet_mode='extended'
                                       )
            if len(tweets) == 0:
                break

            oldest_id = tweets[-1].id
            all_tweets.extend(tweets)

        return self.parse_tweets(all_tweets)

    def parse_tweets(self, tweets):
        """
        Extracts the text from each tweet and stores it in a list.

        :param tweets: (List(Tweets)) A list of tweets for a given user
        :return: (List(String)) A list of the text in each tweet
        """
        all_text = []
        for tweet in tweets:
            tweet_text = tweet.full_text.encode("utf-8").decode("utf-8")
            # Replaces &amp; with & and removes unnecessary spacing
            tweet_text = re.sub(r"&amp;", "&", tweet_text)
            tweet_text = re.sub(r"\s+", " ", tweet_text, flags=re.I)
            tweet_text.strip()

            all_text.append(tweet_text)
        return all_text

    def tweets_to_txt(self, tweets, user_id):
        """
        Saves all given tweets to a txt file with the name userID.txt
            :param tweets: A list of all of a user's tweets
            :param userID: The unique username for a twitter user
        """

        # Encoding is necessary otherwise you encounter charmap error
        with open(user_id + ".txt", 'w', encoding='utf-8') as file:
            for tweet in tweets:
                text = ">>>" + tweet.full_text + "\n"
                file.write(text)
        print("Tweets saved to txt!")
