#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
import string
import pandas as pd

import jiwer
from jiwer import transforms

import nltk
from nltk.corpus import stopwords
nltk.download("stopwords",quiet=True)


# In[11]:


def load_txt_as_string(filepath):
    """Load the filepath"""
    """Return as String"""
    with open(filepath, 'r') as file:
         return file.read()


# In[12]:


def stop_words():
    """Load Stop Words and Remove Needed Ones"""
    stop = stopwords.words('english')
    stop.remove('no')
    stop.remove('not')
    stop.remove('most')
    stop.remove('some')
    stop.remove('out')
    return stop


# In[13]:


def std_abbrev_substitutions(): #medical abbreviation conversion
    """Load the Abbrev and Acronyms"""
    """Return Dictonary of Cleaned Version"""
    acr_abb =pd.read_csv("Acronyms and Abbreviations.csv", header=0)
    abbrev_map = dict(zip(acr_abb['Abbreviation'].str.lower(), acr_abb['Meaning'].str.lower()))
    return abbrev_map


# In[22]:


#textual cleaning and standardization
def text_clean(pres_string,abbrev_map):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    t=jiwer.ExpandCommonEnglishContractions()(pres_string)
    t=jiwer.RemoveKaldiNonWords()(t)
    t= t.translate(translator)
    t=jiwer.Strip()(t)
    t=jiwer.SubstituteWords(abbrev_map)(t)
    t=jiwer.SubstituteWords({"1+": "one plus","1 +": "one plus",
                                 "2 d" :'2d',
                                 "o two": "oxygen saturation", "o2": "oxygen saturation",
                                 'mg': "milligrams",
                                 'x-ray': 'xray',"x ray": "xray", 
                                 'cr td':'crtd',
                                 's 4': 's4','s four':'sfour',
                                 's two':'stwo','s 2': 's2',
                                 's three': ' sthree','s 3': 's3',
                                 'v one':'vone','v 1': 'v1',
                                 't 4':'t4','t four':'tfour',
                                 't 6':'t6','t six':'tsix',
                                 "rails": "rales","rail": "rale"})(t)
    clean_txt=jiwer.RemoveMultipleSpaces()(t)
    return clean_txt


# In[15]:


def clean(filepath):#removes stop words from presentations, applies above cleaning functions
    """Takes in a File Path, i.e txt file"""
    """output is a string"""
    pres_str=load_txt_as_string(filepath)
    stop = stop_words()
    abbrev_map = std_abbrev_substitutions()
    clean_response = text_clean(pres_str,abbrev_map)

    clean_response=[word for word in clean_response.split() if word not in (stop)]
    return " ".join(clean_response)
 


# In[24]:
#Example Clean
#clean_transcript=clean('transcript.txt')
#clean_transcript


# In[26]:

# Write the string to the file
#with open("clean_transcript.txt", "w") as f:
    
    #f.write(clean_transcript)

