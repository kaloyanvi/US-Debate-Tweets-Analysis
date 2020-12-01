# Loading necessary libraries
import pandas as pd
import time
import datetime
from datetime import datetime as dt

def preprocess_data(input_file):

    print("Preprocessing started!")
    # Loading the data
    start_time = time.time()
    start_data = pd.read_csv(input_file, lineterminator='\n')
    print("\nData has been loaded!")

    # No language column in the data, so English tweets selection is removed

    # Converting the time of tweets to datetime objects
    start_data['created_at'] = pd.to_datetime(start_data['created_at'])
    print("\nDates have been transformed to datetime objects!")

    # Making datetime objects of the starting and the ending point of the debate
    debate_start = dt.strptime("2020-10-22 20:30", '%Y-%m-%d %H:%M') # 30 min before start
    debate_end = dt.strptime("2020-10-22 23:00", '%Y-%m-%d %H:%M') # 30 min after end

    # Tweets only from the debate
    tmp_start = start_data[start_data['created_at'] >= debate_start]  # all tweets after the start of the event
    debate_data = tmp_start[tmp_start['created_at'] <= debate_end]  # all tweets after the end of the event
    print("\nSelecting only the tweets duting the debate.")

    # Final touches
    debate_data = debate_data.sort_values(by=['created_at'])  # sorting the tweets chronologically
    debate_data = debate_data.reset_index().drop(columns=["index"])
    debate_data.to_csv("data/debate_tweets.csv")  # making a new csv with the preprocessed data

    print("\nData preprocessing complete! New .csv has been created /data/debate_tweets.csv")
    print("--- %s seconds ---" % (time.time() - start_time))
    return debate_data