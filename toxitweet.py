from twython import Twython
import json
import pandas as pd
from nltk.corpus import stopwords
stopwords = list(stopwords.words("english"))
# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

badWords = pd.read_csv("/swearWords.csv").values

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
screen_names = ["ACCOUNTS TO MONITOR"]
dict_ = {'handle': [], 'date': [], 'text': []}
# Create our query
for user in screen_names:
    query = {'screen_name': user,
            "include_rts": False,
            "count": 100
            }
    # Search tweets
    for status in python_tweets.get_user_timeline(**query):
        dict_['handle'].append(query['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df["text"].replace("(@\S*)|(https:.*)|([^a-zA-z0-9 #*&%$!\.,])","",regex=True, inplace = True)
df["text"].replace("\A\s+|\s+\Z","",regex=True, inplace = True)
df = df[df["text"] != ""]
df["text"] = df["text"].str.split(" ")
badCounter = []
for tweet in df["text"]:
    badCount = 0
    for i,word in enumerate(tweet):
        if word.lower() in stopwords:
            tweet.remove(word)
        if word.lower() in badWords:
            badCount += 1
    badCounter.append(badCount)

df["Toxic"] = badCounter
df.to_csv("/tweets.csv")
