import pandas as pd
from textblob install textblob
from elasticsearch import Elastichsearch
from datetime import datetime
import calendar

tweets = pd.read_csv('./tweets.csv', sep=',')

print(tweets.head(2))
