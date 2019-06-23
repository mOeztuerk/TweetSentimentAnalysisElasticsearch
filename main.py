import pandas as pd
import re
from textblob import TextBlob
from elasticsearch import Elasticsearch
from datetime import datetime
import preprocessor as p # twitterData preprocessor
import calendar

tweets = pd.read_csv('./tweets.csv', sep=',')

# select only interesting fields
data = tweets[['handle', 'text', 'time']]
pd.set_option('expand_frame_repr', False)
pd.options.display.max_colwidth = 100

# lowercase (disable SettingWithCopyWarning if needed)
# data['text'] = data['text'].apply(lambda x: x.lower())


print(data.head(15))



def add_sentiment(polarity):
    """
    Classify Tweet as pos, neg or neut
    """
    if polarity < 0:
        sentiment = "negative"
    elif polarity == 0:
        sentiment = "neutral"
    else:
        sentiment = "positive"
    return sentiment

# create instance of elasticsearch
es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])

data['polarity'] = data.apply(lambda x: TextBlob(x['text']).sentiment.polarity, axis=1)
data['subjectivity'] = data.apply(lambda x: TextBlob(x['text']).sentiment.subjectivity, axis=1)
data['sentiment'] = data.apply(lambda x: add_sentiment(x['polarity']), axis=1)
print(data.head(15))


for index, row in data.iterrows():
    es.index(index="sentiment",
            doc_type="twitter",
            body={"author": row.handle,
                       "date": row.time,
                       "message": row.text,
                       "polarity": row.polarity,
                       "subjectivity": row.subjectivity,
                       "sentiment": row.sentiment})
