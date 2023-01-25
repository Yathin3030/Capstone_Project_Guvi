#importing necessary libraries
import streamlit as st
import pandas as pd
import json
import snscrape.modules.twitter as sntwitter
from datetime import datetime

#Applying the title, header, subheader and text to the project.
st.title("APPLICATION TO SCRAPE TWITTER DATA")
st.header("Python scripting, Data Collection, MongoDB, Streamlit")
st.subheader("Domain : Social Media")
st.write("Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, we want to scrape the data from Twitter. We Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter. This application scrapes twitter data within the time frame")

#Loading MongoDb client
from pymongo import MongoClient
connection_string = st.text_input("Paste your MongoDb connection string here. After editing password press enter")
client = MongoClient(connection_string)

# Enter the hashtag/keyword for Twitter scraping
hashtag = st.text_input("Enter the KEYWORD or HASHTAG to be searched in Twitter")


sd = st.date_input("Enter the start date to fetch")
start_date = sd.strftime("%Y-%m-%d %H:%M:%S")
ed = st.date_input("Enter the end date to fetch")
end_date = ed.strftime("%Y-%m-%d %H:%M:%S")


count = st.number_input("Enter the number of Tweets needs to be scraped", min_value=10.0, max_value=1000.0, value=50.0, step=10.0)
tweets_list1 = []
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(hashtag).get_items()):
  if i>int(count):
    break
  tweets_list1.append([tweet.date, 
                       tweet.id, 
                       tweet.url, 
                       tweet.user.
                       username, 
                       tweet.content, 
                       tweet.replyCount, 
                       tweet.retweetCount, 
                       tweet.lang, 
                       tweet.source, 
                       tweet.likeCount
                    ])


tweets_df1 = pd.DataFrame(tweets_list1, columns = ['Datetime', 
                                                   'ID', 
                                                   'URL',
                                                   'User', 
                                                   'Tweet_Content', 
                                                   'Reply_Count', 
                                                   'Retweet_Count',
                                                   'Language', 
                                                   'Source', 
                                                   'Like_COunt'
                                                ])



tweets_df1["Datetime"] = tweets_df1["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
mask = (tweets_df1['Datetime'] > start_date) & (tweets_df1['Datetime'] <= end_date)
tweets_df1 = tweets_df1.loc[mask]


st.subheader("The scraped data are as below:")
st.write(tweets_df1)


data = tweets_df1.to_dict(orient = "records")
upload = st.button("Upload to MongoDb")
if upload == True:
    db = client["Twitter_scrapping"]
    col = db[hashtag]
    col.insert_many(data)



json_string = json.dumps(data,indent=4, sort_keys=True, default=str)
st.json(json_string, expanded=True)
st.download_button(
    label="Download data as JSON",
    file_name="data.json",
    mime="application/json",
    data=json_string,
)

#@st.cache
def convert_df(tweets_df1):
    return tweets_df1.to_csv().encode('utf-8')
csv = convert_df(tweets_df1)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name= 'Twitter_scrape.csv',
    mime='text/csv'
)
