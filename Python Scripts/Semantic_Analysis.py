import math
import re
from pymongo import MongoClient
import pandas as pd
from newsapi.newsapi_client import NewsApiClient

# the below method cleans the news articles
def CleanNewsText(text_string):

    try:
        # remove the white space from text
        front_trailing_spaces = r"^\s|\s$"
        text_string = re.sub(front_trailing_spaces, "", text_string)

        # remove new line and digits with regular expression
        text_string = text_string.replace(r"\n", " ")

        # white space adjustment
        white_space = r'\s+'
        text_string = re.sub(white_space, ' ', text_string)

        emojis = r'\\u[\da-z]+'
        text_string = re.sub(emojis, '', text_string)

        # remove patterns matching url format
        url = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
        text_string = re.sub(url, 'CLEANED', text_string)

        # remove emojis from articles
        emojis = r'\\u[\da-z]+\\'
        text_string = re.sub(emojis, '', text_string)

    except:

        pass
    return text_string

news_api_key = "284690c79ca04e109644208e3ada8982"
newsapi = NewsApiClient(api_key=news_api_key)

mongpclient = MongoClient('localhost',27017)
database = mongpclient['Assignment3']
news_collection = database['news_collection']

#Keywords = ["Canada","University","Dalhousie University","Halifax","Canada Education","Moncton","Toronto"]

#Storing the news articles in the MongoDB database
'''
for word in Keywords:
    allnews = newsapi.get_everything(q=word, language='en',page_size=100)
    for article in allnews['articles']:
        for keys in article.keys():
            cleared_value = CleanNewsText(article[keys])
            article[keys] = cleared_value
        news_collection.insert_one(article)
'''

#file = open("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\Assignment 3\\Cleaned_news.json","w")

Total_docs = 0

#search keywords list
search_words = ["Canada","University","Dalhousie University","Halifax","Business"]

datawordcount = {'Search Query':[],'Document containing term df':[]}
wordcountdf = pd.DataFrame(datawordcount, columns = ['Search Query','Document containing term df'])

for keyword in search_words:
    count_freq = 0
    news_iterator = news_collection.find()
    for article in news_iterator:
        Total_docs = Total_docs+1
        item = str(article['title'])+str(article['description'])+str(article['content'])

        if keyword.casefold() in item.casefold():
            count_freq = count_freq+1
    wordcountdf = wordcountdf.append({'Search Query': keyword,'Document containing term df':count_freq},ignore_index=True)

print("Total Documents(N): " + str(Total_docs))

add_data = {"Total Documents(N)/Number of documents term appeared (df)":[],"Log10(N/df)":[]}
extradatadf = pd.DataFrame(add_data, columns = ["Total Documents(N)/Number of documents term appeared (df)","Log10(N/df)"])

for item in range(0, len(wordcountdf)):
    string_ratio = str(Total_docs) + "/" + str( wordcountdf.at[item, "Document containing term df"])
    extradatadf.at[item,"Total Documents(N)/Number of documents term appeared (df)"] = string_ratio
    extradatadf.at[item,"Log10(N/df)"] = math.log10(Total_docs/wordcountdf.at[item,"Document containing term df"])

wordcountdf = pd.concat([wordcountdf,extradatadf],axis=1)
#storing the final wordcount dataframe into semantic_data.csv
wordcountdf.to_csv("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\semantic_data.csv",index=False,header=True)
print(wordcountdf)

def Greatest_count(text):

    countval = 0
    highest_Relative_count = 0

    freq_data = {"Article Number":[], "Total Words (M)":[], "Frequency (F)":[], "F/M Ratio":[], "Title":[], "Description":[], "Content":[]}
    freq_df = pd.DataFrame(freq_data, columns=["Article Number", "Total Words (M)", "Frequency (F)", "F/M Ratio", "Title", "Description", "Content"])

    greatest_wordFreq = {"Article Number":[], "Total Words (M)":[], "Frequency (F)":[], "F/M Ratio":[], "Title":[], "Description":[], "Content":[]}
    greatest_wordFreqdf = pd.DataFrame(greatest_wordFreq,columns=["Article Number", "Total Words (M)", "Frequency (F)", "F/M Ratio", "Title", "Description", "Content"])

    news_iterator = news_collection.find()

    for article in news_iterator:
        countval = countval+1
        item = str(article['title']) + str(article['description']) + str(article['content'])
        totalcountwords = len(item.split(" "))
        freqcount = item.casefold().count(text.casefold())
        number = "Article No" + str(countval)
        Freq_count_relative = freqcount / totalcountwords

        freq_df = freq_df.append({"Article Number": number, "Total Words (M)": totalcountwords,"Frequency (F)": freqcount,"F/M Ratio": Freq_count_relative, "Title": article['title'],"Description": article['description'],"Content": article['content']}, ignore_index=True)

        if (highest_Relative_count<Freq_count_relative):
            highest_Relative_count = Freq_count_relative

    print(freq_df)
    #storing the required data into semantic_data2.csv
    freq_df[["Article Number", "Total Words (M)", "Frequency (F)", "F/M Ratio"]].to_csv("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\semantic_data2.csv",index=False,header=True)

    for item in range(0, len(freq_df)):
        if freq_df.at[item, "F/M Ratio"] == highest_Relative_count:
            greatest_wordFreqdf = greatest_wordFreqdf.append(freq_df.iloc[item], ignore_index=True)

    #Storing thr article with highest F/M ratio in semantic_data3.csv and printing it on the console
    greatest_wordFreqdf.to_csv("F:\\MACS\\Term 2\\Data Warehousing and Data Management CSCI 5408\\Assignments\\semantic_data3.csv",index=False,header=True)
    Frequency_dictionary = greatest_wordFreqdf.to_dict()

    print("The Article with Highest F/M Ratio is : \n")
    print(greatest_wordFreqdf[["Title", "Description", "Content"]])

    print("\n")
    print("Title: " + Frequency_dictionary["Title"][0])

    print("\n")
    print("Description: " + Frequency_dictionary["Description"][0])

    print("\n")
    print("Content: ", Frequency_dictionary["Content"][0])

Greatest_count("Canada")