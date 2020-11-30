# Loading necessary libraries
import pandas as pd
import time
import datetime
from datetime import datetime as dt

def preprocess_data(input_file):

    print("Preprocessing started!")
    # Loading the data
    start_time = time.time()
    start_data = pd.read_csv(input_file, sep=";")
    print("\nData has been loaded!")

    # Focusing only on the English tweets
    en_data = start_data[start_data['Language'] == "en"]
    print("\nOnly the English Tweets have been selected.")

    # Tweet metrics
    total_tweets = len(start_data)
    tweets_en_percent = round(len(en_data) / len(start_data) * 100, 2)
    print("\nThe total amount of Tweets is %s, where %s percent are written in English." % (total_tweets, tweets_en_percent))

    # Converting the time of tweets to datetime objects
    en_data['Created-At'] = pd.to_datetime(en_data['Created-At'])
    print("\nDates have been transformed to datetime objects!")

    # Making datetime objects of the starting and the ending point of the debate
    debate_start = dt.strptime("2020-09-29 20:30", '%Y-%m-%d %H:%M') # 30 min before start
    debate_end = dt.strptime("2020-09-29 23:00", '%Y-%m-%d %H:%M') # 30 min after end

    # Tweets only from the debate
    tmp_start = en_data[en_data['Created-At'] >= debate_start]  # all tweets after the start of the event
    debate_data = tmp_start[tmp_start['Created-At'] <= debate_end]  # all tweets after the end of the event
    print("\nSelecting only the tweets duting the debate.")

    # Final touches
    debate_data = debate_data.sort_values(by=['Created-At'])  # sorting the tweets chronologically
    debate_data = debate_data[debate_data['Scoring String'].notna()]  # getting only the tweets that can have sentiment
    debate_data.reset_index().drop(columns=["index"])
    debate_data.to_csv("data/debate_tweets.csv")  # making a new csv with the preprocessed data

    print("\nData preprocessing complete! New .csv has been created /data/debate_tweets.csv")
    print("--- %s seconds ---" % (time.time() - start_time))
    return debate_data