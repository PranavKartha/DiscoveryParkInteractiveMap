from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import HttpResponse

# Packages for Machine Learing Section
import pandas as pd
import numpy as np
import nltk
import string
import re
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import urllib, base64 
from heapq import nlargest
import json
import matplotlib
matplotlib.use('agg')

# Machine Learning Section
def clean_text(text):
    stopwords = nltk.corpus.stopwords.words('english')
    wn = nltk.WordNetLemmatizer()
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [wn.lemmatize(word) for word in tokens if word not in stopwords]
    return text


# Word Analysis


def top5inDict(mydict):
    FiveHighest={key: mydict[key] for key in sorted(mydict,
                 key=mydict.get, reverse=True)[:5]}
    return FiveHighest


def wordCountAnalysis(clean_Text):
    newlist = {}
    for word in clean_Text:
        if word in newlist:
           newlist[word] +=1
        else:
            newlist[word] = 1
    return newlist


def check_exist(input, input_list):
    if input in input_list:
        input_list[input] += 1
    else:
        input_list[input] = 1
    return input_list


# sns.set()
def create_general_image(data, xlabel, ylabel,title):
    data.plot(kind='bar')
    plt.xticks(rotation=0)
    plt.ylabel(xlabel)
    plt.xlabel(ylabel)
    plt.title(title)
    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return uri


def create_word_cloud(data):
    wc = WordCloud(background_color="white",width=1000,height=1000,max_words=20,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(data)
    plt.imshow(wc, interpolation='bilinear')
    plt.title('Top 20 Word WordCloud')
    plt.axis("off")
    plt.margins(x=0, y=0)
    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return uri

def dict_to_series_graph(data):
    df1 = pd.Series(data)
    inputs = [df1, 'Type of Word', 'Count', ' Top5 Word Count']
    graph = create_general_image(inputs[0], inputs[1], inputs[2], inputs[3])
    return graph

# Pages navigation and loading 
def index(request):
    return render(request,'index.html')


def EnterResponse(request):
    errors = Pattern.object.basic_validator(request.POST)
    if len(errors):
	    for key, value in errors.items():
		    messages.error(request, value)
	    return redirect('/')
    else:
        Pattern.object.create(
            Response = request.POST['resp'],
            Trans_Type = request.POST['trans'],
            Area_Visited = request.POST['area'],
            Emotion = request.POST['emotion'],
            Activity = request.POST['activity']
        )
        area = Area.object.filter(Area_name = request.POST['area'])
        if area:
            # check if the area exist in the data schema
            area_dict = area.values()
            Word = json.loads(area_dict[0]['Word_Count'].replace("\'", "\""))
            trans = json.loads(area_dict[0]['Trans_Count'].replace("\'", "\""))
            emotion = json.loads(area_dict[0]['Emotion_Count'].replace("\'", "\""))
            activity = json.loads(area_dict[0]['Activity_Count'].replace("\'", "\""))
            # process the current input 
            current_resp = clean_text(request.POST['resp'])
            current_resp = wordCountAnalysis(current_resp)
            # update the information of the current area
            for text in current_resp:
                if text in Word:
                    Word[text] +=1
                else:
                    Word[text] =1
            trans = check_exist(request.POST['trans'], trans)
            emotion = check_exist(request.POST['emotion'], emotion)
            activity = check_exist(request.POST['activity'], activity)
            top5 = top5inDict(Word)
            # top5_graph = dict_to_series_graph(top5)
            current_Area = Area.object.get(Area_name = request.POST['area'])
            current_Area.Word_Count = Word
            # current_Area.Word_Cloud = create_word_cloud(Word)
            current_Area.Trans_Count = trans
            current_Area.Emotion_Count = emotion
            current_Area.Activity_Count = activity
            current_Area.Top5Word_Count  = top5
            # current_Area.Top5Word_Graph  = top5_graph
            current_Area.save()
        else:
            clean_word = clean_text(request.POST['resp'])
            word_als = wordCountAnalysis(clean_word)
            top5 = top5inDict(word_als)
            # top5_graph = dict_to_series_graph(top5)
            Area.object.create(
                Area_name = request.POST['area'],
                Word_Count = json.dumps(word_als),
                # Word_Cloud = create_word_cloud(word_als),
                Trans_Count = json.dumps({request.POST['trans']:1}),
                Emotion_Count = json.dumps({request.POST['emotion']:1}),
                Activity_Count = json.dumps({request.POST['activity']:1}),
                Top5Word_Count = top5,
                # Top5Word_Graph  = top5_graph

            )

        return redirect('/thankyou/')

def thankpage(request):
    return render(request, 'thankyoupage.html')

def pattern_success(request):
    # data = pd.DataFrame(data = Pattern.object.all().values())
    # print('pattern data')
    # print(data)
    # trans = data.groupby('Trans_Type')['Trans_Type'].size().rename('trans_type')
    # print(trans)
    # trans = [trans, 'Transportation Type', 'Count of Transportation Type', 'Transportation Type Count']

    # emo = data.groupby('Emotion')['Emotion'].size().rename('emotion')
    # print(emo)
    # emo = [emo, 'Emotion Type', 'Count of Emotion Type', 'Emotion Type Count']

    # act = data.groupby('Activity')['Activity'].size().rename('activity')
    # print(act)
    # act = [act, 'Activity Type', 'Count of Activity Type', 'Activity Type Count']
    # trans_image = create_general_image(trans[0], trans[1] , trans[2], trans[3])
    # print(trans_image)
    # emo_image = create_general_image(emo[0], emo[1], emo[2], emo[3])
    # act_image = create_general_image(act[0], act[1], act[2], act[3])
    # context = {
    #     "data": Area.object.all(),
    #     "trans_image": trans_image,
    #     "emo_image": emo_image,
    #     "act_image": act_image
    # }
    return render(request, 'pattern.html')





# def showWordCloud(result):
#     for index, row in result.iterrows():

#     st.write("Location: " + row['Area'])
#     st.text('Word cloud of top 100 words appearance')
#     wc = WordCloud(background_color="white",
#                    width=1000,height=1000,
#                    max_words=100,
#                    relative_scaling=0.5,
#                    normalize_plurals=False).generate_from_frequencies(row['Word_Freq'])
#     plt.imshow(wc, interpolation="bilinear")
#     plt.axis("off")
#     plt.margins(x=0, y=0)


# def VisitedAreaAnalysis(data):
#     df2 = data.groupby('AreaVisited')['AreaVisited'].count()
#     VisitedArea = df2.rename('visit_area')

#     VisitedArea.plot(kind='barh', figsize=(30,10))
#     plt.ylabel('Area Visited')
#     plt.xlabel('Count of visitors')
#     plt.title("Count of visitor in each Area")


# def trans_type(data):
#     df2 = data.explode('Transportation_Type')
#     df2 = df2.groupby('Transportation_Type')['Transportation_Type'].size()

#     trans = trans_type(data).rename('trans_type')
#     trans.plot(kind='bar')
#     plt.xticks(rotation=0)
#     plt.ylabel('Transportation Type')
#     plt.xlabel('Count of transportation type')
#     plt.title("Transportation Type Count")