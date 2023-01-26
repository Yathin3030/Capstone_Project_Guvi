# Twitter Scraping
<div align="center">
  <img src=https://i.ytimg.com/vi/3KaffTIZ5II/maxresdefault.jpg>
</div>
Twitter’s strength is real-time. No other social platform comes close on this front. While Facebook is trying to compete and Snapchat offers a unique perspective on the theme, Twitter remains our best indicator of the wider pulse of the world and what’s happening within it. Therefore scraping Twitter data and analyzing it for predictions outputs crucial information.

In this project streamlit a free and open source framework is used to create a GUI through which Twitter data is scraped, and uploaded to MongoDb database. The application also provides the end user to download the data in 'csv' and 'json' format. This application may come handy for Data-science projects.
## ✨ Features

- 🔥 Upload scraped data to MongoDb database; Generate n number of data which will be automatically uploaded to MongoDb Database.
- 💤 Obtain the scraped data in GUI
- 🚀 Download data with a click of a button in csv and Json format.

## The working of the code
The follwing section describes the working of code.
### Requirements
- Python 3.8 or higher
- Streamlit workframe
- MongoDb Atlas credentials
## Introduction to snscrape
Released on July 8, 2020, snscrape is a scraping tool for social networking services (SNS). It scrapes things like users, user profiles, hashtags, searches, threads, list posts and returns the discovered items without using Twitter’s API.

## Using snscrape
Now, there are two ways of using snscrape

Using the command prompt, terminal (Converting JSON files for Python)
Using Python Wrapper
I prefer the Python Wrapper method because I believe it's easy to interact with data scraping, rather than engaging in a two-step process with the CLI. However, if you’re interested in knowing the process with CLI, you can refer from here.

To explain better, wrappers around functions in Python allows modifying behavior of function or class. Basically, the wrapper wraps a second function to extend the behavior of the wrapped function, without permanently altering it.

<div align="center">
  <img src=https://miro.medium.com/max/1400/1*b7499m8QPju3AH7WUreP2A.webp>
</div>

This image is your guide when deciding which attributes you need. I used only a few of them in my project but would highly recommend getting most of the attributes. The execution time remains the same, regardless of the number of attributes you declare.

**Initially we need to import the following libraries.**
```py
import streamlit as st
import pandas as pd
import json
import snscrape.modules.twitter as sntwitter
from datetime import datetime
```
**The next 4 lines of code is written to give the heading, subheading to the streamlit application**
```py
st.title("APPLICATION TO SCRAPE TWITTER DATA")
st.header("Python scripting, Data Collection, MongoDB, Streamlit")
st.subheader("Domain : Social Media")
st.write("Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, we want to scrape the data from Twitter. We Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter. This application scrapes twitter data within the time frame")
```
**The following code is used to loading Mongo client. Here the code is written such that the end user needs to paste the MogoDb connection link. You need to edit the password of the connection string and press eneter**

```py
connection_string = st.text_input("Paste your MongoDb connection string here. After editing password press enter")
client = MongoClient(connection_string)
```
**Here a text input will be requested from the user to eneter the hashtag/ keyword of which the data will be scraped further.**
```py
hashtag = st.text_input("Enter the KEYWORD or HASHTAG to be searched in Twitter")
```
**Next the date input is asked from the user, streamlit gives the date in datetime.date format. However this will not match the datetime format in Pandas Library. Therfore, the strftime() function is used to convert date and time objects to their string representation.**
```py
sd = st.date_input("Enter the start date to fetch")
start_date = sd.strftime("%Y-%m-%d %H:%M:%S")
ed = st.date_input("Enter the end date to fetch")
end_date = ed.strftime("%Y-%m-%d %H:%M:%S")
```
Using the code, we can scrape 1000 tweets from Twitter user, which is taken from user through streamlit application. I then pulled the <mark>Datetime</mark>, <mark>ID</mark>, <mark>URL</mark>,<mark>User</mark>, <mark>Tweet Content</mark>,<mark>Reply Count</mark>, <mark>Retweet Count</mark>,<mark>Language</mark>,<mark>Source</mark>, <mark>Like Count</mark> attributes from the tweet object.
The scraped data is appended in tweets_list1 as a list. 

```py
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
```
**Using Pandas the appended list is converted into Pandas Data Frame as shown**
```py
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

```
As we need to match the Datetime object (datetime 64[ns]) of pandas with Datetime of streamlit (datetime.date),the strftime() function is used to convert date and time objects to their string representation. 
```py
tweets_df1["Datetime"] = tweets_df1["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
```

In order to select rows between two dates in pandas DataFrame, first, create a boolean mask using <mark>mask = (tweets_df1['Datetime'] > start_date) & (tweets_df1['Datetime'] <= end_date)</mark> to represent the start and end of the date range. Then you select the DataFrame that lies within the range using the <mark>tweets_df1.loc[ ]</mark> method.
```py
mask = (tweets_df1['Datetime'] > start_date) & (tweets_df1['Datetime'] <= end_date)
tweets_df1 = tweets_df1.loc[mask]
```
**To display the scraped date we use the follwing code using streamlit library.**
```py
st.subheader("The scraped data are as below:")
st.write(tweets_df1)
```

**To upload the scraped data to MongoDb, the permission is asked by the user through st.button. As the user clicks the button a new database is created initially by name "Twitter_scrapping". Then the scraped hashtags are stored in the database as new collection, with hashtag input as collection name.**
```py
data = tweets_df1.to_dict(orient = "records")
upload = st.button("Upload to MongoDb")
if upload == True:
    db = client["Twitter_scrapping"]
    col = db[hashtag]
    col.insert_many(data)
```

**The follwing code is written to download the scraped data in json format**
```py
json_string = json.dumps(data,indent=4, sort_keys=True, default=str)
st.json(json_string, expanded=True)
st.download_button(
    label="Download data as JSON",
    file_name="data.json",
    mime="application/json",
    data=json_string,
)
```
**The follwing code is written to download the scraped data in csv format**
```py
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
```

That's it. Enjoy coding!! 
