from twython import Twython
import json
import pandas as pd

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
screen_names = ["ACCOUNTS TO MONITOR"]
dict_ = {'handle': [], 'date': [], 'text': []}
# Create our query
for user in screen_names:
    print(user)
    query = {'screen_name': user,
            "include_rts": False
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
df.to_csv("SAVE LOCATION OF tweets.csv")
