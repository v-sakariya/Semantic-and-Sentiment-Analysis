import json
from pymongo import MongoClient
from cleantext import Cleaning_twitter_data
import pandas as pd

mongpclient = MongoClient('localhost',27017)
database = mongpclient['Assignment3']
twitter_collection = database['senti_analysis']

required_tweets = twitter_collection.find()

#opening the files of positive and negative words from the location of the files
file_negative = open("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\opinion-lexicon-English\\opinion-lexicon-English\\negative-words.txt")
file_positive = open("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\opinion-lexicon-English\\opinion-lexicon-English\\positive-words.txt")

count = 0
all_the_positive_lines = file_positive.readlines()
all_the_negative_lines = file_negative.readlines()
positiveWords = []
negativeWords = []

#creating a list of positive and negative words
for word in all_the_positive_lines:
    positiveWords.append(word[:-1])

for word in all_the_negative_lines:
    negativeWords.append(word[:-1])

print(positiveWords)
print(negativeWords)

#creating a dataframe for the tweet, Message, Matching words, Polarity of the tweets
data = {'Tweet':[],'Message/tweets':[],'Match':[],'Polarity':[]}

df = pd.DataFrame(data, columns = ['Tweet','Message/tweets','Match','Polarity'])

for tweet in required_tweets:
    count+=1
    print(count)
    cleaned_text = Cleaning_twitter_data(tweet['full_text'])
    positiveMatch = []
    negativeMatch = []
    bagofwords = []
    Polarity = ""
    for word in cleaned_text.split(" "):
        flag = 0
        if word.lower() in positiveWords:
            flag=1
            positiveMatch.append(word)
        if word.lower() in negativeWords:
            flag=1
            negativeMatch.append(word)
        if flag == 1:
            bagofwords.append(word)

    if len(positiveMatch) > len(negativeMatch):
        Polarity = "positive"
    elif len(positiveMatch) < len(negativeMatch):
        Polarity = "negative"
    else:
        Polarity = "neutral"
    my_match_string = ','.join(bagofwords)
    df = df.append({'Tweet':count,'Message/tweets':cleaned_text,'Match': my_match_string,'Polarity':Polarity},ignore_index=True)

    print(positiveMatch)
    print(negativeMatch)
#storing the dataframe into sentiment_data.csv
df.to_csv("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\sentiment_data.csv",index=False,header=True)


