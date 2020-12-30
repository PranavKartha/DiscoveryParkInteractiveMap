import streamlit as st
import pandas as pd
import numpy as np
# from arcgis.gis import GIS
# from arcgis.mapping import WebMap
import nltk
import string
import re
import seaborn as sns
# import plotly.express as px
import matplotlib.pyplot as plt
# import mysql.connector
import MySQLdb
from heapq import nlargest
from PIL import Image
from wordcloud import WordCloud
import json

# st.title('Discovery Park Interaction Pattern')

# DATA_COLUMN ='date/time'

# mygis = GIS("https://fodp.maps.arcgis.com", "FoDP1974", "n5BTt4F94Q")
# parkmap = mygis.content.get('18eb7e27020e46728f0bcff528832401')
# discoverypark= WebMap(parkmap)
# with st.echo():

# @st.cache
# def load_data():
sqlcnx = MySQLdb.connect(user='root',
                         password='root',
                         host = 'localhost',
                         port=3306,
                         database='InteractionPatternDB')
pattern_data = pd.read_sql('select * from park_pattern', sqlcnx)
area_data = pd.read_sql('select * from park_area', sqlcnx)
sns.set(font_scale=1.4)
st.title('DiscoveryPark Analysis')
# data = pd.read_csv('Test.csv', encoding= 'unicode_escape')
stopwords = nltk.corpus.stopwords.words('english')
wn = nltk.WordNetLemmatizer()
# df = gpd.read_file('discoverylandmarks.csv')
st.header('Word Count Analysis')
for index, row in area_data.iterrows():
    # fig, axs = plt.subplots(1, figsize=(20, 10), nrow=2)
    st.write("Location: " + row['Area_name'])
    st.text('Word cloud of top 100 words appearance')
    wordcount = json.loads(row['Word_Count'].replace("\'", "\""))
    wc = WordCloud(background_color="white",width=1000,height=1000, max_words=100,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(wordcount)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    st.pyplot()
    st.text('Top 5 words appearance')
    top5 = json.loads(row['Top5Word_Count'].replace("\'", "\""))
    plt.bar(*zip(*top5.items()))
    st.pyplot()
# Step 1
# Analyze where did people go when the visit the park
st.header('Visited Area Analysis')
VisitedArea = pattern_data.groupby('Area_Visited')['Area_Visited'].count()
VisitedArea.plot(kind='barh', figsize=(30,10))
plt.ylabel('Area Visited')
plt.xlabel('Count of visitors')
plt.title("Count of visitor in each Area")
st.pyplot()


# Step2
# Analyze what their transportation type to get to discovery park             
st.header('Transportation Type Analysis')
trans = pattern_data.groupby('Trans_Type')['Trans_Type'].size()
trans.plot(kind='bar')
plt.xticks(rotation=0)
plt.ylabel('Transportation Type')
plt.xlabel('Count of Transportation Type')
plt.title("Transportation Type Count")
st.pyplot()

# Step3
# Analyze the emotion while they are visiting the park
st.header('Emotion Type Analysis')
emo = pattern_data.groupby('Emotion')['Emotion'].size()  
emo.plot(kind='bar')
plt.xticks(rotation=0)
plt.ylabel('Emotion Type')
plt.xlabel('Count of Emotion Type')
plt.title("Emotion Type Count")
st.pyplot()

# Step4
# Analysis the activity they do while in the park
st.header('Activity Type Analysis')
act = pattern_data.groupby('Activity')['Activity'].size()
act.plot(kind='bar')
plt.xticks(rotation=0)
plt.ylabel('Activity Type')
plt.xlabel('Count of Activity Type')
plt.title("Activity Type Count")
st.pyplot()