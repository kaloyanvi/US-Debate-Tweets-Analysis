import os
import numpy as np
import pandas as pd

def preprocessingDebate(file_path):

    df_initial_debate = pd.read_csv(file_path)

    # Making new dataframe which wont have repeating speakers that are the same person

    speakers = []
    minutes = []
    texts = []

    for index in range(len(df_initial_debate)-1):

        # debate attributes
        speaker = df_initial_debate.iloc[index].speaker
        minute = df_initial_debate.iloc[index].minute
        current_text = df_initial_debate.iloc[index].text
        next_speaker = df_initial_debate.iloc[index+1].speaker
        next_text = df_initial_debate.iloc[index+1].text

        try:
            # checking if the current speaker is the last speaker
            if speaker == df_initial_debate.iloc[index-1].speaker:
                # checking if the current speaker is also a next speaker
                if speaker == next_speaker:
                    texts[-1] += " " + next_text
                    continue # skipping to next iteration
                else:
                    continue # skipping to next iteration
        
        except: # avoiding for the first row because there cant be previous speaker
                pass 
        
        if speaker == next_speaker: 
            #  combining the text of the current speaker and next if same
            speakers.append(speaker)
            minutes.append(minute)
            texts.append(current_text + " " + next_text)

        else:
            #  text only of current speaker given next one is different
            speakers.append(speaker)
            minutes.append(minute)
            texts.append(current_text)

    debate_data = {"speaker":speakers,"minute":minutes,"text":texts}
    df_debate = pd.DataFrame(debate_data)

    df_debate['num_words'] = df_debate['text'].str.split().str.len()
    df_debate['minute']=pd.to_datetime(df_debate['minute'], format='%M:%S')

    # Interruptions
    df_debate['time_between']=0
    df_debate['interrupted']=0
    for i in range(0, 72):
        df_debate['time_between'][i] = (df_debate.iloc[i+1]['minute']-df_debate.iloc[i]['minute']).total_seconds()
    for i in range(0, 72):
        time = (df_debate['time_between'][i]<=60 & df_debate['time_between'][i+1]<=60)
        trump_biden = ((df_debate['speaker'][i]=='Donald Trump') & (df_debate['speaker'][i+1]=='Joe Biden'))
        biden_trump = ((df_debate['speaker'][i]=='Joe Biden') & (df_debate['speaker'][i+1]=='Donald Trump'))
        speakers = (trump_biden | biden_trump)
        if (time):
            df_debate['interrupted'][i]=1
        if (time & speakers):
            df_debate['interrupted'][i]=2 

    return df_debate
    #df_debate.to_csv("../data/debate_preprocessed.csv")